# This file will handle all asset loading and initialization
import os
import pygame

# Initialize pygame mixer before loading assets
pygame.mixer.init()

# Update asset paths to be absolute based on the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
SQUARE_IMAGE_PATH = os.path.join(script_dir, 'assets', 'square.png')
POWER_UP_IMAGE_PATH = os.path.join(script_dir, 'assets', 'power_up.png')
SQUARE_CLICK_SOUND = os.path.join(script_dir, 'assets', 'square_click.wav')
POWER_UP_SOUND = os.path.join(script_dir, 'assets', 'power_up.wav')
GAME_OVER_SOUND = os.path.join(script_dir, 'assets', 'game_over.wav')

# Define constants for asset dimensions
POWER_UP_SIZE = 50

def load_assets():
    global square_image, power_up_image, square_click_sound, power_up_sound, game_over_sound
    square_image = pygame.image.load(SQUARE_IMAGE_PATH)
    power_up_image = pygame.image.load(POWER_UP_IMAGE_PATH)
    square_image = pygame.transform.scale(square_image, (50, 50))
    # Ensure the power-up image matches the dimensions of its rectangle
    power_up_image = pygame.transform.scale(power_up_image, (POWER_UP_SIZE, POWER_UP_SIZE))
    square_click_sound = pygame.mixer.Sound(SQUARE_CLICK_SOUND)
    power_up_sound = pygame.mixer.Sound(POWER_UP_SOUND)
    game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

# Ensure assets are loaded before importing variables
load_assets()