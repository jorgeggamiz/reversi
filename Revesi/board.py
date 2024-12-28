from config import SIZE

def new_board():
    board=[[' '  for _ in range(SIZE)] for _ in range(SIZE)]

    for i in range(SIZE):
        for j in range(SIZE):
            board[i][j]=' '
    
    return board


def restart_board(board):
    for i in range(SIZE):
        for j in range(SIZE):
            board[i][j]=' '
    
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def copy_board(board):
    copy = new_board()

    for i in range(SIZE):
        for j in range(SIZE):
            copy[i][j]=board[i][j]
    
    return copy