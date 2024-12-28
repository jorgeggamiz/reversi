from board import SIZE

def score(board):
    scoreX=0
    scoreO=0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j]=='X': scoreX+=1
            elif board[i][j]=='O': scoreO+=1
    
    return {'X':scoreX, 'O':scoreO}

def show_score(board):
    scores = score(board)
    print(f"X:{scores['X']}, O:{scores['O']}")