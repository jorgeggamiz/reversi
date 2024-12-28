import random
from reversi import *
from config import SIZE

MAX_DEPTH = 4    

def count_tokens(board, token):
    count=0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j]==token: count+=1
    
    return count


def count_corners(board, token):
    count=0

    if board[0][0]==token: count+=1
    if board[SIZE-1][0]==token: count+=1
    if board[0][SIZE-1]==token: count+=1
    if board[SIZE-1][SIZE-1]==token: count+=1

    return count


def count_values(board, token):
    count = 0

    values = [
        [25, -5, 15, 10, 10, 15, -5, 25],
        [-5, -10, -4, 2, 2, -4, -10, -5],
        [15, -4, 3, 4, 4, 3, -4, 15],
        [10, 2, 4, 0, 0, 4, 2, 10],
        [10, 2, 4, 0, 0, 4, 2, 10],
        [15, -4, 3, 4, 4, 3, -4, 15],
        [-5, -10, -4, 2, 2, -4, -10, -5],
        [25, -5, 15, 10, 10, 15, -5, 25]
    ]
    
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == token:
                count+=values[i][j]
    
    return count


def heuristic(board, token):
    value=0
    rival_token='O' if token=='X' else 'X'
    num_rival_tokens = count_tokens(board, rival_token)
    num_tokens = count_tokens(board, token)

    if num_rival_tokens==0: value=float('inf')-1
    elif num_tokens==0: value=float('-inf')+1
    elif is_game_over(board):
        if num_tokens < num_rival_tokens: value=float('-inf')+1
        elif num_tokens > num_rival_tokens: value=float('inf')-1
    else:
        #######
        # First factor: how many pieces does each player have
        if num_tokens > num_rival_tokens:
            value += 20*num_tokens/(num_tokens+num_rival_tokens)
        elif num_tokens < num_rival_tokens:
            value += 20*num_rival_tokens/(num_tokens+num_rival_tokens)

        #######
        # Second factor: possesion of the corners
        num_corners = count_corners(board, token)
        num_rival_corners = count_corners(board, rival_token)
        value += 500*(num_corners-num_rival_corners)

        #######
        # Third factor: value of the positions occupied by each player
        value_pos_player = count_values(board, token)
        value_pos_rival = count_values(board, rival_token)
        total = value_pos_player + value_pos_rival

        if total!=0:
            if value_pos_player > value_pos_rival:
                value += 75*(value_pos_player/total)
            elif value_pos_player < value_pos_rival:
                value += -75*(value_pos_rival/total)

    return value 


def minimax(board, depth, maximizing, token):
    if depth==MAX_DEPTH or is_game_over(board):
        return -1, -1, heuristic(board, token)
    
    rival_token = 'O' if token=='X' else 'X'
    xmove, ymove = -1,1

    if maximizing:
        best_value=float('-inf')
        valid_plays = get_valid_plays(board, token)
        for x,y in valid_plays:
            copy = copy_board(board)
            make_a_play(copy, token, x, y)
            _,_,value = minimax(copy, depth+1, False, token)
            if value>best_value:
                best_value=value
                if depth==0:
                    xmove,ymove = x,y
        
        return xmove, ymove, best_value
    else:
        best_value=float('inf')
        valid_plays = get_valid_plays(board, rival_token)
        for x,y in valid_plays:
            copy = copy_board(board)
            make_a_play(copy, rival_token, x, y)
            _,_,value = minimax(copy, depth+1, True, token)
            best_value = min(best_value, value)
        
        return -1, -1, best_value
    

def random_play(board, token):
    valid_plays = get_valid_plays(board, token)
    random.shuffle(valid_plays)
    return valid_plays[0]

def intelligent_play(board, token):
    x,y,_ = minimax(board, 0, True, token)
    return [x,y]
    