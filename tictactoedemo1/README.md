# Tic-Tac-Toe Game

A simple console-based Tic-Tac-Toe game implemented in Python for two players.

## Features

- **Two-player gameplay**: Players X and O take turns
- **Input validation**: Prevents invalid moves and provides clear error messages
- **Win detection**: Automatically detects winning conditions and draws
- **Multiple games**: Option to play multiple rounds
- **Clear interface**: Easy-to-read board display with position references

## How to Play

1. **Run the game**:
   ```
   python tictactoe.py
   ```

2. **Game Rules**:
   - Players take turns placing their marks (X or O) on a 3x3 grid
   - Enter a number from 1-9 to place your mark in the corresponding position:
     ```
     1 | 2 | 3
     -----------
     4 | 5 | 6
     -----------
     7 | 8 | 9
     ```
   - First player to get three marks in a row (horizontally, vertically, or diagonally) wins
   - If all 9 spaces are filled without a winner, the game is a draw

3. **Input Format**:
   - Enter numbers 1-9 when prompted
   - Invalid inputs (letters, numbers outside 1-9, or occupied positions) will prompt you to try again

4. **Playing Multiple Games**:
   - After each game, you'll be asked if you want to play again
   - Enter 'y' or 'yes' to start a new game
   - Enter 'n' or 'no' to exit

## Example Gameplay

```
========================================
      Welcome to Tic-Tac-Toe!
========================================

 Position Numbers:
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 

 Current Board:
   |   |   
-----------
   |   |   
-----------
   |   |   

Player X, enter your move (1-9): 5

 Current Board:
   |   |   
-----------
   | X |   
-----------
   |   |   

Player O, enter your move (1-9): 1
...
```

## Requirements

- Python 3.x
- No additional libraries required

## Files

- `tictactoe.py`: Main game implementation
- `plan.md`: Development plan and design decisions
- `README.md`: This file with usage instructions

## Code Structure

The game is implemented using a `TicTacToe` class with the following key methods:

- `display_board()`: Shows the current game state
- `make_move()`: Places a player's mark on the board
- `check_winner()`: Determines if there's a winner
- `play_game()`: Main game loop
- `play_multiple_games()`: Handles multiple game sessions

Enjoy playing Tic-Tac-Toe! 🎮
