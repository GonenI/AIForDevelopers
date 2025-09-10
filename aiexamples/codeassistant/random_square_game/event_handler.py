# This file will handle all event-related logic
import pygame
import time
from assets import square_click_sound, power_up_sound, game_over_sound
from constants import POWER_UP_DURATION

def handle_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            game_over_sound.play()  # Play sound when game ends
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.bullets > 0:
                game.bullets -= 1  # Decrease bullets on click
                mouse_pos = event.pos
                for square in game.squares[:]:
                    if square["rect"].collidepoint(mouse_pos):
                        if game.power_up_active:
                            game.score += 20  # Double points when power-up is active
                        else:
                            game.score += 10
                        game.squares.remove(square)
                        square_click_sound.play()  # Play sound when square is clicked
                # Revert the expanded clickable area for power-ups
                for power_up in game.power_ups[:]:
                    if power_up["rect"].collidepoint(mouse_pos):
                        print(f"Power-up clicked at {mouse_pos}")  # Debugging output
                        game.power_ups.remove(power_up)
                        game.power_up_active = True
                        game.power_up_end_time = time.time() + POWER_UP_DURATION
                        game.score += 50  # Add an immediate score bonus
                        power_up_sound.play()  # Play sound when power-up is collected
            if game.bullets == 0 and game.squares:
                game.running = False  # End game if out of bullets and squares remain
                game_over_sound.play()