import random

def print_board(board):
    print(" 0 | 1 | 2 ")
    print("-----------")
    print(" 3 | 4 | 5 ")
    print("-----------")
    print(" 6 | 7 | 8 ")

    print("The current board:")
    print(" {} | {} | {} ".format(board[0], board[1], board[2]))
    print("-----------")
    print(" {} | {} | {} ".format(board[3], board[4], board[5]))
    print("-----------")
    print(" {} | {} | {} ".format(board[6], board[7], board[8]))

def check_winner(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            return board[i]

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            return board[i]

    # Check diagonals
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]

    # Check if it's a tie
    if ' ' not in board:
        return 'Tie'

    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X': return -10
    elif winner == 'O': return 10
    elif winner == 'Tie': return 0

    if is_maximizing:
        best_score = -1000
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -1000
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def main():
    board = [' ' for _ in range(9)]
    print_board(board)
    while True:
        user_move = int(input("Enter your move (0-8): "))
        if board[user_move] == ' ':
            board[user_move] = 'X'
            print_board(board)

            winner = check_winner(board)
            if winner:
                if winner == 'Tie':
                    print("It's a tie!")
                else:
                    print(f"{winner} wins!")
                break

            computer_move = find_best_move(board)
            board[computer_move] = 'O'
            print_board(board)

            winner = check_winner(board)
            if winner:
                if winner == 'Tie':
                    print("It's a tie!")
                else:
                    print(f"{winner} wins!")
                break
        else:
            print("Invalid move. Try again.")

main()