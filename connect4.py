'''
CONNECT FOUR GAME
by Alexander Munoz
'''

import random
import itertools

class Game():
    def __init__(self, size=7, ai_bool=False):
        self.tokens = ['_']
        self.player_names = []
        self.player_colors = []
        self.size = size
        self.board = [[self.tokens[0] for i in range(self.size)] for j in range(self.size)]
        self.curr_player = random.choice([1,2])
        self.moves_played = 0
        self.possible_transitions = list(itertools.product([-1,0,1], [-1,0,1]))
        self.possible_transitions.remove((0,0))
        self.ai = ai_bool

    def setup(self):
        self.__askUser("Player 1 name: ", name_flag=True)
        self.__askUser("Player 1 token: ", token_flag=True)
        self.__askUser("Player 1 color ('R', 'B', 'G', 'Y', 'P'): ", color_flag=True)
        if self.ai:
            self.player_names = self.player_names + ['AI_BOT']
            self.tokens = self.tokens + ['*']
            random_color = random.choice(list(set(['R', 'B', 'G', 'Y', 'P'])-set(self.player_colors)))
            self.player_colors = self.player_colors + [random_color]
            print "Player 2 (%s) will have token %s and color %s" % \
                  (self.player_names[1], self.tokens[2], self.player_colors[1])
        else:
            self.__askUser("Player 2 name: ", name_flag=True)
            self.__askUser("Player 2 token: ", token_flag=True)
            self.__askUser("Player 2 color ('R', 'B', 'G', 'Y', 'P'): ", color_flag=True)
        launch_text = "Player %i was randomly selected to begin. Press enter to play!" % self.curr_player
        self.__askUser(launch_text)

    def __askUser(self, text, name_flag=False, token_flag=False, color_flag=False, num_flag=False):
        ''' ask user for input '''
        while True: # get player 2 token
            try:
                print text,
                user_in = raw_input()
                if name_flag and len(user_in)>0:
                    self.player_names = self.player_names + [user_in]
                    return
                elif token_flag and len(user_in)==1:
                    self.tokens = self.tokens + [user_in]
                    return
                elif color_flag and (user_in in ['R', 'B', 'G', 'Y', 'P']):
                    self.player_colors = self.player_colors + [user_in]
                    return
                elif num_flag and 1<=int(user_in)<=self.size and self.board[0][int(user_in)-1]==self.tokens[0]:
                    return int(user_in)-1
                elif all([not a for a in [name_flag, token_flag, color_flag, num_flag]]):
                    return
                else:
                    print "Invalid entry. Please try again."
            except Exception:
                print "Invalid entry. Please try again."

    def __getUserMove(self):
        ''' ask player which column they would like to move to '''
        print self.player_names[self.curr_player-1] + ' it\'s your turn.'
        col = self.__askUser('Which column? ', num_flag=True)
        return col

    def __colorPrint(self, player_num, text):
        ''' prints in players color '''
        if self.player_colors[player_num] == 'R':
            print '\033[91m' + text + '\033[0m',
        elif self.player_colors[player_num] == 'B':
            print '\033[94m' + text + '\033[0m',
        elif self.player_colors[player_num] == 'G':
            print '\033[92m' + text + '\033[0m',
        elif self.player_colors[player_num] == 'Y':
            print '\033[93m' + text + '\033[0m',
        elif self.player_colors[player_num] == 'P':
            print '\033[95m' + text + '\033[0m',

    def displayBoard(self):
        ''' print the board to the terminal '''
        print
        for i in range(self.size):
            print i+1,
            print " ",
        print
        for row in self.board:
            for elt in row:
                if elt[0] == self.tokens[1]:
                    self.__colorPrint(0, elt[0])
                elif elt[0] == self.tokens[2]:
                    self.__colorPrint(1, elt[0])
                else:
                    print elt[0],
                print " ",
            print
        print

    def move(self, ai_in=None):
        ''' call __getUserMove or user AI input,
            then add a players symbol to that column at the
            lowest possible row available. Return values as follows:
            0 : neither player has won, and there are still empty cells
            1 : player1 won the game
            2 : player2 won the game
            3 : tie, all cells filled '''
        if ai_in is None:
            col_selected = self.__getUserMove()
        else:
            col_selected = ai_in
            print self.player_names[self.curr_player-1] + ' moves to column ' + str(ai_in+1) + '.'
        row_options = range(self.size)[::-1]
        for row_option in row_options:
            if self.board[row_option][col_selected] == self.tokens[0]:
                self.board[row_option][col_selected] = self.tokens[self.curr_player]
                if self.__checkEndGame(row_option,col_selected,self.board):
                    return self.curr_player
                self.moves_played += 1
                if self.moves_played >= self.size * self.size:
                    return 3
                self.curr_player = 1 if self.curr_player == 2 else 2
                return 0

    def __validPos(self, row_num, col_num):
        ''' check to see if a row and col pair are inside of the board '''
        return 0 <= row_num < self.size and 0 <= col_num < self.size

    def __checkEndGame(self, curr_row, curr_col, board):
        ''' check to see if the games is over, returns true if player who moved
            last won the game, else returns false. Input is the row and column
            selected by the player's most recent move (a win must involve this
            tile)'''
        curr_token = self.tokens[self.curr_player]
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

    def endGame(self, verdict):
        ''' ends game with following possible inputs -
            1 : player1 won the game
            2 : player2 won the game
            3 : tie, all cells have been filled '''
        if verdict == 1 or verdict == 2:
            print '\n\n\n\n\n'
            winning_statement = '!!' + self.player_names[verdict-1].upper() + ' WINS!!'
            self.__colorPrint(verdict-1, winning_statement)
            print '\n\n\n\n\n'
        elif verdict == 3:
            print '\n\n\n\n\n'
            print 'TIED GAME - ALL CELLS ARE FULL!'
            print '\n\n\n\n\n'
