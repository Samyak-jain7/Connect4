from __future__ import division
from connect4 import Game
import numpy as np
from copy import deepcopy
import time

class MiniMax():
    def __init__(self, tokens, possible_transitions, size, reward_connections, \
                 min_think_time, min_depth, discount):
        self.tokens = tokens
        self.possible_transitions = possible_transitions
        self.size = size
        self.reward_connections = reward_connections
        self.min_think_time = min_think_time
        self.min_depth = min_depth
        self.discount = discount
        self.index = 2 #AI is always player 2

    def __validPos(self, row_num, col_num):
        ''' check to see if a row and col position pair is inside of the board '''
        return 0 <= row_num < self.size[0] and 0 <= col_num < self.size[1]

    def __checkEndGame(self, curr_row, curr_col, board):
        ''' check to see if the games is over, returns true if player who moved
            last won the game, else returns false. Input is the row and column
            selected by the player's most recent move (a win must involve this
            tile)'''
        if curr_row is None or curr_col is None: #initial setup, not endgame
            return False
        curr_token = board[curr_row][curr_col]
        for t1,t2 in self.possible_transitions:
            if self.__validPos(curr_row+t1, curr_col+t2) and board[curr_row+t1][curr_col+t2] == curr_token:
                if self.__validPos(curr_row+2*t1,curr_col+2*t2) and board[curr_row+2*t1][curr_col+2*t2] == curr_token:
                    if self.__validPos(curr_row+3*t1,curr_col+3*t2) and board[curr_row+3*t1][curr_col+3*t2] == curr_token:
                        return True
                    elif self.__validPos(curr_row-t1,curr_col-t2) and board[curr_row-t1][curr_col-t2] == curr_token:
                            return True
                elif self.__validPos(curr_row-t1,curr_col-t2) and board[curr_row-t1][curr_col-t2] == curr_token:
                    if self.__validPos(curr_row-2*t1,curr_col-2*t2) and board[curr_row-2*t1][curr_col-2*t2] == curr_token:
                        return True
        return False

    def __generateSuccessors(self, board, curr_player):
        ''' generate successor boards '''
        poss_cols = [i for i, e in enumerate(board[0]) if e == self.tokens[0]]
        poss_cols = sorted(poss_cols, key=lambda item:np.abs(item-self.size[1]/2))
        successors = [deepcopy(board) for i in range(len(poss_cols))]
        row_options = range(self.size[0])[::-1]
        selected_rows = []
        for board_num in range(len(successors)):
            for row_option in row_options:
                if successors[board_num][row_option][poss_cols[board_num]] == self.tokens[0]:
                    successors[board_num][row_option][poss_cols[board_num]] = self.tokens[curr_player]
                    selected_rows.append(row_option)
                    break
        return zip(selected_rows, poss_cols, successors)

    def __getDiags(self, board):
        ''' adapted from https://stackoverflow.com/a/31373955/190597 '''
        h, w = len(board), len(board[0])
        return [[board[h - p + q - 1][q]
                 for q in range(max(p-h+1, 0), min(p+1, w))]
                 for p in range(h + w - 1)] + \
               [[board[p - q][q]
                 for q in range(max(p-h+1,0), min(p+1, w))]
                 for p in range(h + w - 1)]

    def __countConnections(self, board):
        ''' calculate the number of possible connections on the board '''
        connections = 0
        for i in range(self.size[0]):
            row = board[i]
            connections -= sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[1])>=3 and \
                                   [w,x,y,z].count(self.tokens[2])==0,
                                   zip(row, row[1:], row[2:], row[3:])))
            connections += sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[2])>=3 and \
                                   [w,x,y,z].count(self.tokens[1])==0,
                                   zip(row, row[1:], row[2:], row[3:])))
        for i in range(self.size[1]):
            col = [r[i] for r in board]
            connections -= sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[1])>=3 and \
                                   [w,x,y,z].count(self.tokens[2])==0,
                                   zip(col, col[1:], col[2:], col[3:])))
            connections += sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[2])>=3 and \
                                   [w,x,y,z].count(self.tokens[1])==0,
                                   zip(col, col[1:], col[2:], col[3:])))
        diags = filter(lambda y: len(y)>=4, self.__getDiags(board))
        for diag in diags:
            connections -= sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[1])>=3 and \
                                   [w,x,y,z].count(self.tokens[2])==0,
                                   zip(diag, diag[1:], diag[2:], diag[3:])))
            connections += sum(map(lambda (w,x,y,z): \
                                   [w,x,y,z].count(self.tokens[2])>=3 and \
                                   [w,x,y,z].count(self.tokens[1])==0,
                                   zip(diag, diag[1:], diag[2:], diag[3:])))
        return connections

    def __scoreState(self, board, endGameBool, curr_player, depth, max_depth):
        ''' calculate reward for a board configuration '''
        if endGameBool: #if endgame, large positive/negative reward
            reward = 1e6 if curr_player!=self.index else -1e6
        elif self.reward_connections: #reward is number of tiles connected
            reward = self.__countConnections(board)
        else: #no reward if not endgame
            reward = 0
        steps = max_depth - depth
        discounted = reward * (1+self.discount)**(-1*steps)
        return discounted

    def __minimaxCalc(self, board, moves_played, depth, max_depth, row, col, alpha, beta, curr_player):
        ''' run minimax algorithm '''
        endGameBool = self.__checkEndGame(row, col, board)
        if endGameBool or moves_played>=self.size[0]*self.size[1] or depth<=0:
            reward = self.__scoreState(board, endGameBool, curr_player, depth, max_depth)
            return reward, None
        successors = self.__generateSuccessors(board, curr_player)
        next_player = 1 if curr_player==2 else 2
        if curr_player == self.index: #max agent
            bestValue, bestAction = -np.inf, None
            for nextrow, nextcol, nextboard in successors:
                v, _ = self.__minimaxCalc(nextboard, moves_played+1, depth, max_depth, \
                                          nextrow, nextcol, alpha, beta, next_player)
                bestAction = nextcol if v>bestValue else bestAction
                bestValue = v if v>bestValue else bestValue
                alpha = max(alpha, bestValue)
                if beta < alpha:
                    break
            return bestValue, bestAction
        else: #min agent
            bestValue = np.inf
            for nextrow, nextcol, nextboard in successors:
                v, _ = self.__minimaxCalc(nextboard, moves_played+1, depth-1, max_depth, \
                                          nextrow, nextcol, alpha, beta, next_player)
                bestValue = v if v<bestValue else bestValue
                beta = min(beta, bestValue)
                if beta < alpha:
                    break
            return bestValue, None

    def pickColumn(self, board, moves_played):
        ''' run minimax with iterative deepening '''
        depth = 0
        t_0 = time.time()
        while (time.time()-t_0<=self.min_think_time or depth<self.min_depth)\
              and depth*2<=self.size[0]*self.size[1]-moves_played:
            depth += 1
            v, a = self.__minimaxCalc(board, moves_played, depth, depth, None, None, -np.inf, np.inf, self.index)
        return v, a, depth, time.time()-t_0
