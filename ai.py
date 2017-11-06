from connect4 import Game
import numpy as np
from copy import deepcopy

class MiniMax():
    def __init__(self, tokens, possible_transitions, size=7):
        self.tokens = tokens
        self.size = size
        self.index = 2 #AI is always player 2
        self.possible_transitions = possible_transitions

    def __validPos(self, row_num, col_num):
        ''' check to see if a row and col position pair is inside of the board '''
        return 0 <= row_num < self.size and 0 <= col_num < self.size

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
        poss_cols = sorted(poss_cols, key=lambda item:np.abs(item-self.size/2))
        successors = [deepcopy(board) for i in range(len(poss_cols))]
        row_options = range(self.size)[::-1]
        selected_rows = []
        for board_num in range(len(successors)):
            for row_option in row_options:
                if successors[board_num][row_option][poss_cols[board_num]] == self.tokens[0]:
                    successors[board_num][row_option][poss_cols[board_num]] = self.tokens[curr_player]
                    selected_rows.append(row_option)
                    break
        return zip(selected_rows, poss_cols, successors)

    def __minimaxCalc(self, board, moves_played, depth, row, col, alpha, beta, curr_player):
        if self.__checkEndGame(row, col, board):
            reward = 5*1.1**(-1*moves_played) if curr_player!=self.index else -1
            return reward, None
        elif moves_played >= self.size * self.size or depth<=0:
            reward = 0
            return reward, None
        successors = self.__generateSuccessors(board, curr_player)
        next_player = 1 if curr_player==2 else 2
        if curr_player == self.index: #max agent
            bestValue, bestAction = -np.inf, None
            for nextrow, nextcol, nextboard in successors:
                v, _ = self.__minimaxCalc(nextboard, moves_played+1, depth, \
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
                v, _ = self.__minimaxCalc(nextboard, moves_played+1, depth-1, \
                                          nextrow, nextcol, alpha, beta, next_player)
                bestValue = v if v<bestValue else bestValue
                beta = min(beta, bestValue)
                if beta < alpha:
                    break
            return bestValue, None

    def pickColumn(self, board, moves_played, depth=3):
        ''' pick a column '''
        v, a = self.__minimaxCalc(board, moves_played, depth, None, None, -np.inf, np.inf, 2)
        return v, a
