import pygame
from game import gon_Game

def gon_main():
    pygame.init()
    game = gon_Game()
    game.gon_run()
    pygame.quit()

if __name__ == "__main__":
    gon_main()
