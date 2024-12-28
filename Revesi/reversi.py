from board import *
from config import SIZE


def valid_pos(x,y):
    return x>=0 and x<=SIZE-1 and y>=0 and y<=SIZE-1


def empty_pos(board,x,y):
    return board[x][y]==' '


def is_a_corner(x,y):
    return (x==0 and y==0) or (x==SIZE-1 and y==0) or (x==0 and y==SIZE-1) or (x==SIZE-1 and y==SIZE-1)


def valid_play(board, token, initx, inity):
    if not empty_pos(board, initx, inity) or not valid_pos(initx,inity):
        return False
    
    board[initx][inity] = token
    rival_token = 'O' if token=='X' else 'X'
    changing_tokens=[]

    # To change the necessary tokens, we'll have to move in all eight possible directions (up, down, left, right and four diagonals)
    for directionx, directiony in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x,y = initx,inity
        x += directionx # first step in the direction
        y += directiony # first step in the direction

        if valid_pos(x,y) and board[x][y]==rival_token:
            x+=directionx
            y+=directiony

            if not valid_pos(x,y): continue

            while board[x][y] == rival_token:
                x+=directionx
                y+=directiony
                
                if not valid_pos(x,y): break

            if not valid_pos(x,y): continue

            if board[x][y] == token: # We have to convert all the tokens we've been passing
                while True:
                    x-=directionx
                    y-=directiony

                    if x==initx and y==inity: break

                    changing_tokens.append([x,y])
    
    board[initx][inity] = ' '
    
    if len(changing_tokens) == 0: return False
    return changing_tokens

def get_valid_plays(board, token):
    valid_plays = []
    for i in range(SIZE):
        for j in range(SIZE):
            if valid_play(board, token, i, j):  # Check if the play is valid
                valid_plays.append((i, j))
    return valid_plays


def make_a_play(board, token, initx, inity):
    changing_tokens = valid_play(board, token, initx, inity)

    if changing_tokens==False: return False

    board[initx][inity] = token
    for i,j in changing_tokens:
        board[i][j] = token
    
    return True


def is_game_over(board):
    count=0
    
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j]!=' ': count+=1

    if count==SIZE**2: 
        return True
    elif not get_valid_plays(board, 'X') and not get_valid_plays(board, 'O'):
        return True
    else: 
        return False