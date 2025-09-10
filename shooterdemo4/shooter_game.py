import pygame
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Target:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.radius = 40
        self.inner_radius = 20
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y
            
        # Keep target within bounds
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def draw(self, screen):
        # Draw outer red circle
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        # Draw inner white circle
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.inner_radius)
        # Draw center point
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)
    
    def is_hit(self, mouse_x, mouse_y):
        # Calculate distance between mouse click and target center
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius
    
    def get_hit_score(self, mouse_x, mouse_y):
        # Calculate distance between mouse click and target center
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        if distance <= 5:  # Center hit
            return 100
        elif distance <= self.inner_radius:  # Inner circle hit
            return 50
        elif distance <= self.radius:  # Outer circle hit
            return 10
        else:
            return 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter Game - Click to Shoot!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Create sound effects using built-in pygame sounds
        self.hit_sound = self.create_hit_sound()
        self.miss_sound = self.create_miss_sound()
        
        self.score = 0
        self.target = Target()
        self.running = True
        self.hit_effect = []  # For visual feedback on hits
        
    def create_hit_sound(self):
        # Create a simple pleasant beep sound for hits
        try:
            # Try to create a programmatic sound
            sample_rate = 22050
            duration = 0.2
            frequency = 800  # High pitch for success
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                t = float(i) / sample_rate
                wave = int(4096 * math.sin(frequency * 2 * math.pi * t) * (1 - t/duration))
                arr.extend([wave, wave])  # Stereo
            
            # Convert to bytes
            sound_buffer = bytes()
            for sample in arr:
                # Convert to 16-bit signed integer
                if sample > 32767:
                    sample = 32767
                elif sample < -32768:
                    sample = -32768
                sound_buffer += sample.to_bytes(2, byteorder='little', signed=True)
            
            # Create sound from buffer
            sound = pygame.mixer.Sound(buffer=sound_buffer)
            return sound
        except:
            # Fallback to silence if sound creation fails
            return pygame.mixer.Sound(buffer=b'\x00' * 1000)
    
    def create_miss_sound(self):
        # Create a lower pitch buzz sound for misses
        try:
            sample_rate = 22050
            duration = 0.3
            frequency = 150  # Low pitch for failure
            
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                t = float(i) / sample_rate
                # Add some distortion
                wave = int(3000 * math.sin(frequency * 2 * math.pi * t) * (1 - t/duration))
                wave += int(1000 * math.sin(frequency * 3 * 2 * math.pi * t))  # Harmonic
                arr.extend([wave, wave])  # Stereo
            
            # Convert to bytes
            sound_buffer = bytes()
            for sample in arr:
                # Convert to 16-bit signed integer
                if sample > 32767:
                    sample = 32767
                elif sample < -32768:
                    sample = -32768
                sound_buffer += sample.to_bytes(2, byteorder='little', signed=True)
            
            # Create sound from buffer
            sound = pygame.mixer.Sound(buffer=sound_buffer)
            return sound
        except:
            # Fallback to silence if sound creation fails
            return pygame.mixer.Sound(buffer=b'\x00' * 1000)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    self.shoot(mouse_x, mouse_y)
    
    def shoot(self, mouse_x, mouse_y):
        if self.target.is_hit(mouse_x, mouse_y):
            hit_score = self.target.get_hit_score(mouse_x, mouse_y)
            self.score += hit_score
            
            # Play hit sound
            self.hit_sound.play()
            
            # Add hit effect
            self.hit_effect.append({
                'x': mouse_x,
                'y': mouse_y,
                'score': hit_score,
                'timer': 60,  # Show for 1 second at 60 FPS
                'color': GREEN if hit_score > 0 else RED
            })
            
            # Create new target
            self.target = Target()
        else:
            # Play miss sound
            self.miss_sound.play()
            
            # Miss effect
            self.hit_effect.append({
                'x': mouse_x,
                'y': mouse_y,
                'score': 0,
                'timer': 30,
                'color': RED
            })
    
    def update(self):
        self.target.move()
        
        # Update hit effects
        self.hit_effect = [effect for effect in self.hit_effect if effect['timer'] > 0]
        for effect in self.hit_effect:
            effect['timer'] -= 1
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw target
        self.target.draw(self.screen)
        
        # Draw hit effects
        for effect in self.hit_effect:
            if effect['score'] > 0:
                # Hit effect - show score
                score_text = self.font.render(f"+{effect['score']}", True, effect['color'])
                self.screen.blit(score_text, (effect['x'] - 20, effect['y'] - 30))
            else:
                # Miss effect - show X
                miss_text = self.font.render("MISS", True, effect['color'])
                self.screen.blit(miss_text, (effect['x'] - 25, effect['y'] - 15))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions
        instruction_text = self.font.render("Click on the target to shoot!", True, WHITE)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw crosshair at mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, WHITE, (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
        pygame.draw.line(self.screen, WHITE, (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
