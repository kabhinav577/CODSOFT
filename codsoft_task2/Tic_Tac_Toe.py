import math

# Initialize board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Display the board
def print_board():
    print()
    for row in board:
        print('|'.join(row))
        print('-' * 5)
    print()

# Check for winner
def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != ' ':
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != ' ':
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != ' ':
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != ' ':
        return b[0][2]
    return None

# Check if board is full
def is_full():
    return all(cell != ' ' for row in board for cell in row)

# Minimax with alpha-beta pruning
def minimax(depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_full():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

# AI makes a move
def ai_move():
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(0, False, -math.inf, math.inf)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = 'O'

# Human move
def human_move():
    while True:
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if board[row][col] == ' ':
                board[row][col] = 'X'
                break
            else:
                print("Cell already taken!")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

# Main game loop
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X', AI is 'O'")
    print_board()

    while True:
        human_move()
        print_board()
        if check_winner(board) == 'X':
            print("You win!")
            break
        if is_full():
            print("It's a draw!")
            break

        print("AI's turn...")
        ai_move()
        print_board()
        if check_winner(board) == 'O':
            print("AI wins!")
            break
        if is_full():
            print("It's a draw!")
            break

# Run the game
play_game()
