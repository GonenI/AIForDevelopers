import pygame
import pygame.time
import random
import time
from constants import WIDTH, HEIGHT, WHITE, BLUE, RED, SPAWN_RATE, POWER_UP_SIZE, POWER_UP_DURATION, POWER_UP_COLOR
from assets import load_assets, square_image, power_up_image, square_click_sound, power_up_sound, game_over_sound
from event_handler import handle_events
from drawing import draw

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize mixer before loading assets
        load_assets()  # Load assets after mixer initialization
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Random Square Game")
        self.default_font = pygame.font.Font(None, 36)
        self.score = 0
        self.running = True
        self.squares = []
        self.power_ups = []
        self.power_up_active = False
        self.power_up_end_time = 0
        self.clock = pygame.time.Clock()  # Use pygame.time.Clock explicitly
        self.bullets = 10  # Add a new attribute for bullets

    def create_square(self):
        size = 50
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        return {
            "rect": pygame.Rect(x, y, size, size),
            "spawn_time": time.time()
        }

    def create_power_up(self):
        size = POWER_UP_SIZE
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        return {
            "rect": pygame.Rect(x, y, size, size),
            "spawn_time": time.time()
        }

    def update_squares(self):
        current_time = time.time()
        for square in self.squares[:]:
            if current_time - square["spawn_time"] > 5:
                self.squares.remove(square)
        if self.power_up_active and time.time() > self.power_up_end_time:
            self.power_up_active = False
        # Replenish bullets when all squares are cleared
        if not self.squares and self.bullets < 10:
            self.bullets = 10

    def run(self):
        while self.running:
            handle_events(self)
            if len(self.squares) < 5 and random.random() < SPAWN_RATE:
                self.squares.append(self.create_square())
            if len(self.power_ups) < 1 and random.random() < 0.01:
                self.power_ups.append(self.create_power_up())
            self.update_squares()
            draw(self)
            self.clock.tick(30)  # Use the updated clock object
        pygame.quit()