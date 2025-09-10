import pygame
from target import gon_Target
from score import gon_Score

class gon_Game:
    def __init__(self):
        self.gon_screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Shooter Game")
        self.gon_clock = pygame.time.Clock()
        self.gon_target = gon_Target(800, 600)
        self.gon_score = gon_Score()
        self.gon_running = True

    def gon_run(self):
        while self.gon_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gon_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gon_target.gon_check_hit(event.pos):
                        self.gon_score.gon_increment()
                        self.gon_target.gon_reset()

            self.gon_target.gon_update()
            self.gon_screen.fill((30, 30, 30))
            self.gon_target.gon_draw(self.gon_screen)
            self.gon_score.gon_draw(self.gon_screen)
            pygame.display.flip()
            self.gon_clock.tick(60)
