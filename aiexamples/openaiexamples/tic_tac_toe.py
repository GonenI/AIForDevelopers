import random

from openai import OpenAI
client = OpenAI()

#                You will be presented with the board state as a string of 9 digits, \
#                representing the state of the board going left to right, top to bottom\
#                where the value of each position indicates the following: 0 for untaken space, 1 for 'X', and 2 for 'O'. \
#                For example 100000020 means an X in the NW corner, an O in the S corner, and the rest of the board is empty.\

def get_computer_move(boardstate) -> int:
    response = client.chat.completions.create(
        model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You will be presented with a tic-tac-toe board on the turn of 'O'\
                suggest the best next move for 'O' to beat 'X' \
                your response should only be a single or two characters of your next move slot position (one of the following NW, N, NE, W, C, E, SW, S, SE)\
                do not move to a slot that is already occupied by an 'X' or an 'O', do not make a move that will allow 'X' to win during his next move.\
                three X's or O's in a row, column, or diagonal wins the game.\
                For your convenience, here are all possible winning combinations:\
                ['NW', 'N', 'NE'],['W', 'C', 'E'],['SW', 'S', 'SE'],['NW', 'W', 'SW'],['N', 'C', 'S'],['NE', 'E', 'SE'],['NW', 'C', 'SE'],['NE', 'C', 'SW']"                
        },
        {
            "role": "user",
            "content": boardstate
        }
        ],
        temperature=1,
        max_tokens=150,
        top_p=0.5
    )
    print("response = ", response.choices[0].message.content)
    return response.choices[0].message.content


def get_board_string(board):
    board_string = f" {board['NW']}  |  {board['N']}  |  {board['NE']}  \n"
    board_string += "----------------\n"
    board_string += f" {board['W']}  |  {board['C']}  |  {board['E']}  \n"
    board_string += "----------------\n"
    board_string += f" {board['SW']}  |  {board['S']}  |  {board['SE']}  \n"
    return board_string

def available_moves(board):
    return [k for k, v in board.items() if v == ' ']

def check_winner(board, player):
    win_conditions = [
        ['NW', 'N', 'NE'],
        ['W', 'C', 'E'],
        ['SW', 'S', 'SE'],
        ['NW', 'W', 'SW'],
        ['N', 'C', 'S'],
        ['NE', 'E', 'SE'],
        ['NW', 'C', 'SE'],
        ['NE', 'C', 'SW']
    ]
    return any(all(board[pos] == player for pos in condition) for condition in win_conditions)

def play_game():
    position_list = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    board = {pos: ' ' for pos in position_list}
    print(get_board_string(board))
    
    while True:
        user_move = input("Make your move:  [NW,N,NE,W,C,E,SW,S,SE]\n").strip().upper()
        if user_move not in available_moves(board):
            print("Invalid move. Try again.")
            continue
        
        board[user_move] = 'X'
        if check_winner(board, 'X'):
            print(get_board_string(board))
            print("Congratulations! You win!")
            break

        if not available_moves(board):
            print(get_board_string(board))
            print("It's a draw!")
            break
        
        # generate a string of the board state using 9 digits going left to right, top to bottom where 0 is empty, 1 is X, and 2 is O
        #board_state = ''.join(['0' if pos == ' ' else '1' if pos == 'X' else '2' for pos in board.values()])    

        board_state = get_board_string(board)   

        print (board_state)

        # computer_move = random.choice(available_moves(board))

        # computer_move_pos = get_computer_move(board_state)
        # translate pos to direction    
        #computer_move = position_list[computer_move_pos]

        computer_move = get_computer_move(board_state)

        print(f"Computer moves to {computer_move}")

        board[computer_move] = 'O'
        if check_winner(board, 'O'):
            print(get_board_string(board))
            print("You lose. Better luck next time!")
            break
        
        print(get_board_string(board))

play_game()
