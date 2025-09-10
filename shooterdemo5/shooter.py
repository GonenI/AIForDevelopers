
import pygame
import random
import sys
import numpy as np

# Initialize pygame
pygame.init()

def make_beep(frequency, duration_ms, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    wave = np.sin(frequency * 2 * np.pi * t)
    audio = (wave * (2**15 - 1) * volume).astype(np.int16)
    # Convert mono to stereo by duplicating the array
    stereo_audio = np.column_stack((audio, audio))
    sound = pygame.sndarray.make_sound(stereo_audio)
    return sound

hit_sound = make_beep(880, 120, 0.7)  # High beep
miss_sound = make_beep(220, 120, 0.7) # Low beep

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Demo")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Target properties
TARGET_RADIUS = 40
BAND_WIDTH = 10
TARGET_SPEED = 3

def draw_target(surface, x, y):
    # Draw cocentric circles (red and white bands)
    for i in range(TARGET_RADIUS, 0, -BAND_WIDTH):
        color = RED if ((TARGET_RADIUS - i) // BAND_WIDTH) % 2 == 0 else WHITE
        pygame.draw.circle(surface, color, (x, y), i)

def main():
    clock = pygame.time.Clock()
    score = 0
    missed = 0
    font_big = pygame.font.SysFont(None, 72)
    font_label = pygame.font.SysFont(None, 56)

    # Initial target position and direction
    target_x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    target_y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    current_speed = TARGET_SPEED
    dx = random.choice([-current_speed, current_speed])
    dy = random.choice([-current_speed, current_speed])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                dist = ((mx - target_x) ** 2 + (my - target_y) ** 2) ** 0.5
                if dist <= TARGET_RADIUS:
                    hit_sound.play()
                    score += 1
                    current_speed += 1
                    target_x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
                    target_y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
                    dx = random.choice([-current_speed, current_speed])
                    dy = random.choice([-current_speed, current_speed])
                else:
                    miss_sound.play()
                    missed += 1

        # Move target
        target_x += dx
        target_y += dy
        # Bounce off walls
        if target_x <= TARGET_RADIUS or target_x >= WIDTH - TARGET_RADIUS:
            dx = -dx
        if target_y <= TARGET_RADIUS or target_y >= HEIGHT - TARGET_RADIUS:
            dy = -dy

        screen.fill(BLACK)
        draw_target(screen, target_x, target_y)

        # Draw labels
        score_label = font_label.render("SCORE", True, GREEN)
        missed_label = font_label.render("MISSED", True, RED)
        screen.blit(score_label, (40, 30))
        screen.blit(missed_label, (WIDTH - missed_label.get_width() - 40, 30))

        # Draw values
        score_value = font_big.render(str(score), True, GREEN)
        missed_value = font_big.render(str(missed), True, RED)
        screen.blit(score_value, (60, 110))
        screen.blit(missed_value, (WIDTH - missed_value.get_width() - 60, 110))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
