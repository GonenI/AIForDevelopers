import pygame

class gon_Score:
    def __init__(self):
        self.gon_score = 0
        self.gon_font = pygame.font.SysFont(None, 48)

    def gon_increment(self):
        self.gon_score += 1

    def gon_draw(self, gon_screen):
        text = self.gon_font.render(f"Score: {self.gon_score}", True, (255, 255, 255))
        gon_screen.blit(text, (10, 10))
