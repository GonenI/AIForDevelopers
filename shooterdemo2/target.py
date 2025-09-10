import pygame
import random

class gon_Target:
    def __init__(self, gon_screen_width, gon_screen_height):
        self.gon_screen_width = gon_screen_width
        self.gon_screen_height = gon_screen_height
        self.gon_radius = 30
        self.gon_color = (200, 50, 50)
        self.gon_reset()

    def gon_reset(self):
        self.gon_x = random.randint(self.gon_radius, self.gon_screen_width - self.gon_radius)
        self.gon_y = random.randint(self.gon_radius, self.gon_screen_height - self.gon_radius)
        self.gon_dx = random.choice([-5, 5])
        self.gon_dy = random.choice([-5, 5])

    def gon_update(self):
        self.gon_x += self.gon_dx
        self.gon_y += self.gon_dy
        if self.gon_x <= self.gon_radius or self.gon_x >= self.gon_screen_width - self.gon_radius:
            self.gon_dx *= -1
        if self.gon_y <= self.gon_radius or self.gon_y >= self.gon_screen_height - self.gon_radius:
            self.gon_dy *= -1

    def gon_draw(self, gon_screen):
        pygame.draw.circle(gon_screen, self.gon_color, (self.gon_x, self.gon_y), self.gon_radius)

    def gon_check_hit(self, pos):
        mx, my = pos
        return (mx - self.gon_x) ** 2 + (my - self.gon_y) ** 2 <= self.gon_radius ** 2
