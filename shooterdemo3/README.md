# Shooter Game

A simple Python shooter game where you try to hit a bouncing target with mouse clicks.

## Game Features

- **Bouncing Target**: A red circular target that bounces around the screen
- **Mouse Shooting**: Click anywhere on the screen to shoot
- **Score Tracking**: Earn points for each successful hit
- **Accuracy Statistics**: Track your shots fired and accuracy percentage
- **Visual Effects**: See shooting effects and crosshairs for better gameplay

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Run the game using:
```bash
python main.py
```

## How to Play

1. A red target with a white border and crosshair will appear and start bouncing around the screen
2. Click on the target with your mouse to score points
3. Each successful hit increases your score by 1 point
4. The target will reset to a new random position after each hit
5. Your score, total shots, and accuracy percentage are displayed in the top-left corner
6. Close the window to exit the game

## Game Controls

- **Left Mouse Button**: Shoot at the target
- **Close Window**: Exit the game

## Project Structure

The game follows the Single Responsibility Principle (SRP) with separate classes:

- `src/game.py` - Main game controller and game loop
- `src/target.py` - Target object with bouncing movement
- `src/player.py` - Player input and shooting mechanics  
- `src/score.py` - Score tracking and display
- `main.py` - Entry point to start the game

## Development

All functions follow the naming convention with the `gon_` prefix as specified in the project requirements.

Enjoy playing the Shooter Game!
