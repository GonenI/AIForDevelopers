import pygame
from game import Game

def main():
    try:
        print
        pygame.mixer.init()  # Ensure mixer is initialized before anything else
    except pygame.error as e:
        print(f"Failed to initialize mixer: {e}")
        exit(1)  # Exit if mixer initialization fails

    pygame.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    print
    main()