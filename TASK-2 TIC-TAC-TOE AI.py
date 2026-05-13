import math

# Constants for players
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

def print_board(board):
    for i, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("-----------")

def check_winner(b):
    # Check rows, columns, and diagonals
    win_states = [
        [b[0][0], b[0][1], b[0][2]], [b[1][0], b[1][1], b[1][2]], [b[2][0], b[2][1], b[2][2]],
        [b[0][0], b[1][0], b[2][0]], [b[0][1], b[1][1], b[2][1]], [b[0][2], b[1][2], b[2][2]],
        [b[0][0], b[1][1], b[2][2]], [b[2][0], b[1][1], b[0][2]]
    ]
    if [AI, AI, AI] in win_states: return 10
    if [HUMAN, HUMAN, HUMAN] in win_states: return -10
    return 0

def is_moves_left(board):
    return any(EMPTY in row for row in board)

def minimax(board, depth, is_max, alpha, beta):
    score = check_winner(board)
    
    if score == 10: return score - depth # AI wins
    if score == -10: return score + depth # Human wins
    if not is_moves_left(board): return 0 # Draw

    if is_max:
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[r][c] = EMPTY
                    alpha = max(alpha, best)
                    if beta <= alpha: break
        return best
    else:
        best = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[r][c] = EMPTY
                    beta = min(beta, best)
                    if beta <= alpha: break
        return best

def find_best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[r][c] = EMPTY
                if move_val > best_val:
                    move = (r, c)
                    best_val = move_val
    return move

# Main Game Loop
def play_game():
    board = [[EMPTY]*3 for _ in range(3)]
    print("Tic-Tac-Toe: Human (X) vs AI (O)")
    
    while is_moves_left(board) and check_winner(board) == 0:
        print_board(board)
        # Human Turn
        try:
            move = int(input("Enter move (1-9): ")) - 1
            r, c = divmod(move, 3)
            if board[r][c] != EMPTY: raise ValueError
        except (ValueError, IndexError):
            print("Invalid move! Try again.")
            continue
        
        board[r][c] = HUMAN
        if not is_moves_left(board) or check_winner(board) != 0: break
        
        # AI Turn
        print("\nAI is thinking...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = AI

    print_board(board)
    result = check_winner(board)
    if result == 10: print("AI wins! Better luck next time.")
    elif result == -10: print("You won! (Wait, that shouldn't happen...)")
    else: print("It's a draw!")

if __name__ == "__main__":
    play_game()