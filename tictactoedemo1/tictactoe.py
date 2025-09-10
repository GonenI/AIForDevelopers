class TicTacToe:
    def __init__(self):
        """Initialize the game with an empty 3x3 board."""
        self.board = [' ' for _ in range(9)]  # 9 empty spaces
        self.current_player = 'X'
    
    def display_board(self):
        """Display the current state of the board."""
        print("\n Current Board:")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("-----------")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("-----------")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print()
    
    def display_positions(self):
        """Display the position numbers for reference."""
        print("\n Position Numbers:")
        print(" 1 | 2 | 3 ")
        print("-----------")
        print(" 4 | 5 | 6 ")
        print("-----------")
        print(" 7 | 8 | 9 ")
        print()
    
    def is_valid_move(self, position):
        """Check if the move is valid (position is empty and in range)."""
        return 1 <= position <= 9 and self.board[position - 1] == ' '
    
    def make_move(self, position):
        """Place the current player's mark on the board."""
        if self.is_valid_move(position):
            self.board[position - 1] = self.current_player
            return True
        return False
    
    def check_winner(self):
        """Check if there's a winner."""
        # Define winning combinations (indices)
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' '):
                return self.board[combo[0]]  # Return the winner ('X' or 'O')
        
        return None  # No winner yet
    
    def is_board_full(self):
        """Check if the board is completely filled."""
        return ' ' not in self.board
    
    def reset_board(self):
        """Reset the board for a new game."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
    
    def switch_player(self):
        """Switch between X and O players."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_player_move(self):
        """Get and validate player input."""
        while True:
            try:
                move = int(input(f"Player {self.current_player}, enter your move (1-9): "))
                if self.is_valid_move(move):
                    return move
                else:
                    print("Invalid move! Position is either occupied or out of range.")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 9.")
    
    def play_game(self):
        """Main game loop."""
        print("=" * 40)
        print("      Welcome to Tic-Tac-Toe!")
        print("=" * 40)
        
        while True:
            self.display_positions()
            self.display_board()
            
            # Get player move
            move = self.get_player_move()
            
            # Make the move
            self.make_move(move)
            
            # Check for winner
            winner = self.check_winner()
            if winner:
                self.display_board()
                print(f"🎉 Player {winner} wins! 🎉")
                break
            
            # Check for draw
            if self.is_board_full():
                self.display_board()
                print("🤝 It's a draw! 🤝")
                break
            
            # Switch to the other player
            self.switch_player()
    
    def play_multiple_games(self):
        """Allow playing multiple games."""
        while True:
            self.play_game()
            
            # Ask if players want to play again
            while True:
                play_again = input("\nDo you want to play again? (y/n): ").lower()
                if play_again in ['y', 'yes']:
                    self.reset_board()
                    print("\n" + "=" * 40)
                    print("      Starting New Game!")
                    print("=" * 40)
                    break
                elif play_again in ['n', 'no']:
                    print("Thanks for playing! Goodbye! 👋")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")


def main():
    """Main function to start the game."""
    game = TicTacToe()
    game.play_multiple_games()


if __name__ == "__main__":
    main()
