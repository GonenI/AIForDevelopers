import random





def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(all(cell != " " for cell in row) for row in board)

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        while True:
            coordinates = input("Enter row and column (e.g., 1,2): ")
            try:
                row, col = map(int, coordinates.split(","))
                if row in range(3) and col in range(3):
                    break
                else:
                    print("Coordinates must be between 0 and 2. Try again.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by a comma.")
        row, col = map(int, coordinates.split(","))

        if board[row][col] == " ":
            board[row][col] = current_player
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            elif is_full(board):
                print_board(board)
                print("It's a tie!")
                break
            current_player = "O" if current_player == "X" else "X"
        else:
            print("Cell already taken, try again.")

if __name__ == "__main__":
    # tell the user that the game is starting
    print("Welcome to Tic Tac Toe!")

    # print a welcome message for the user
    


    # start the game
    tic_tac_toe()

