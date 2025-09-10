"""
Main entry point for the Shooter Game.
This file initializes and starts the game.
"""

from src.game import Game


def gon_main():
    """Main function to start the shooter game."""
    try:
        # Create and run the game
        game = Game()
        print("Starting Shooter Game...")
        print("Instructions:")
        print("- Click on the red target to score points")
        print("- The target bounces around the screen")
        print("- Try to get the highest score possible!")
        print("- Close the window to exit")
        print()
        
        game.gon_run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you have pygame installed: pip install pygame")
    finally:
        print("Thanks for playing!")


if __name__ == "__main__":
    gon_main()
