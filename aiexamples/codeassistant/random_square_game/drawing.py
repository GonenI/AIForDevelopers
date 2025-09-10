# This file will handle all drawing-related logic
import pygame
from constants import WHITE, BLUE, RED, POWER_UP_COLOR, HEIGHT, WIDTH
from assets import square_image, power_up_image

def draw(game):
    game.screen.fill(WHITE)
    for square in game.squares:
        game.screen.blit(square_image, (square["rect"].x, square["rect"].y))  # Draw square using image
    for power_up in game.power_ups:
        game.screen.blit(power_up_image, (power_up["rect"].x, power_up["rect"].y))  # Draw power-up using image
    score_text = game.default_font.render(f"Score: {game.score}", True, BLUE)
    game.screen.blit(score_text, (10, 10))
    if game.power_up_active:
        power_up_text = game.default_font.render("Power-Up Active!", True, POWER_UP_COLOR)
        game.screen.blit(power_up_text, (WIDTH // 2 - 100, 10))
    # Draw bullets
    for i in range(game.bullets):
        bullet_rect = pygame.Rect(10 + i * 15, HEIGHT - 30, 10, 10)
        pygame.draw.rect(game.screen, RED, bullet_rect)
    pygame.display.flip()