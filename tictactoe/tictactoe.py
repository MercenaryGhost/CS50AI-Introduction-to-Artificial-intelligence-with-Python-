"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    a=0;b=0
    for i in range(3):
        a=a+board[i].count(X)
        b=b+board[i].count(O)
    if a==0 and b==0:
        return X
    elif a>b:
        return O
    else:
        return X
    #raise NotImplementedError
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = []
    possible = set(possible)
    
    for i in range(3):
        for j in range(3):
            if (board[i][j] == EMPTY):
                possible.add((i,j))
    
    if len(possible) == 0:
        possible.add((1,1))
    
    return possible
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy
    temp = copy.deepcopy(board)
    ply = player(temp)
    
    if action[0]<0 or action[0]>2 or action[1]<0 or action[1]>2:
        raise Exception('Play within the board!')
        
    if temp[action[0]][action[1]] is not EMPTY:
        raise Exception('Invalid move!')
        
    temp[action[0]][action[1]] = ply
    return temp
    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    flag = 0
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        flag = 1
        return X
    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        flag = 1
        return O
    else:
        for i in range(3):
            if (board[i][0] == X and board[i][1] == X and board[i][2] == X) or (board[0][i] == X and board[1][i] == X and board[2][i] == X):
                flag = 1
                return X
            if (board[i][0] == O and board[i][1] == O and board[i][2] == O) or (board[0][i] == O and board[1][i] == O and board[2][i] == O):
                flag = 1
                return O
    if flag == 0:
        return None
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result = winner(board)
    if result is not None:
        return True
    elif board[0].count(EMPTY) == 0 and board[1].count(EMPTY) == 0 and board[2].count(EMPTY) == 0:
        return True
    else:
        return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else:
        return 0
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None
    ply = player(board)
    if board == initial_state() and ply == X:
        return (0,2)   # I have explicitly given this state because even without this if condition AI plays this move at first. By giving this condition I can avoid the major processing time at the beginning. Because it evaluates every possiblie move at the beginning and the likely moves are however all the cells give it same utility = 0 so all are equally optimal (AI is X). 
    def maximum(board):
        if terminal(board):
            return utility(board)
        v = -100
        for action in actions(board):
            v = max(v,minimum(result(board,action)))
        return v
    
    def minimum(board):
        if terminal(board):
            return utility(board)
        v = 100
        for action in actions(board):
            v = min(v,maximum(result(board,action)))
        return v
    
    max_utility = -100
    min_utility = 100
    opt_action = 0
    if ply == X:
        for action in actions(board):
            result1 = result(board,action)
            if winner(result1) == X:
                return action
        for action in actions(board):
            if minimum(result1) >= max_utility:
                max_utility = minimum(result(board,action))
                opt_action = action
        return opt_action
    else:
        for action in actions(board):
            result1 = result(board,action)
            if winner(result1) == O:
                return action
        for action in actions(board):
            result1 = result(board,action)            
            if maximum(result1) <= min_utility:
                min_utility = maximum(result(board,action))
                opt_action = action
        return opt_action
    #raise NotImplementedError
