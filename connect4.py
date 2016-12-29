'''
CONNECT FOUR GAME
by Alexander Munoz
'''

import random

##### FLAGS #####
tokens = ['_']
player_names = []
player_colors = []
size = 7

# initialize
board = []
curr_player = 1
moves_played = 0
possible_transitions = []

# print in color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_print(player_num, text):
    ''' prints in players color given 0 for player 1 or 1 for player 2
        and text to print'''
    if player_colors[player_num] == 'R':
        print bcolors.FAIL + text + bcolors.ENDC,
    elif player_colors[player_num] == 'B':
        print bcolors.OKBLUE + text + bcolors.ENDC,
    elif player_colors[player_num] == 'G':
        print bcolors.OKGREEN + text + bcolors.ENDC,
    elif player_colors[player_num] == 'Y':
        print bcolors.WARNING + text + bcolors.ENDC,
    elif player_colors[player_num] == 'P':
        print bcolors.HEADER + text + bcolors.ENDC,

def initialize_game():
    ''' iniitialize board to list with underscores for empty cells,
        initialize with player names and tokens,
        randomly pick player to start '''
    global board, size, possible_transitions, curr_player
    print
    while True: # get player 1 name
        try:
            print "Player 1 name (wrapped in quotes): ",
            name = input()
            if len(name) > 0:
                player_names.append(name)
                break
            else:
                print "Please type a valid name. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid name. Don't forget to wrap in quotes!"
    while True: # get player 1 token
        try:
            print "Player 1 token symbol (wrapped in quotes): ",
            token = input()
            if len(token) == 1:
                tokens.append(token)
                break
            else:
                print "Please type a valid, single-character token symbol. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid, single-character token symbol. Don't forget to wrap in quotes!"
    while True: # get player 1 color
        try:
            print "Player 1 color ('R' for red, 'B' for blue, 'G' for green, 'Y' for yellow, 'P' for pink): ",
            color = input()
            if color == 'R' or color == 'B' or color == 'G' or color == 'Y' or color == 'P':
                player_colors.append(color)
                break
            else:
                print "Please type a valid color symbol. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid color symbol. Don't forget to wrap in quotes!"
    while True: # get player 2 name
        try:
            print "Player 2 name (wrapped in quotes): ",
            name = input()
            if len(name) > 0:
                player_names.append(name)
                break
            else:
                print "Please type a valid name. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid name. Don't forget to wrap in quotes!"
    while True: # get player 2 token
        try:
            print "Player 2 token symbol (wrapped in quotes): ",
            token = input()
            if len(token) == 1:
                tokens.append(token)
                break
            else:
                print "Please type a valid, single-character token symbol. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid, single-character token symbol. Don't forget to wrap in quotes!"
    while True: # get player 2 color
        try:
            print "Player 2 color ('R' for red, 'B' for blue, 'G' for green, 'Y' for yellow, 'P' for pink): ",
            color = input()
            if color == 'R' or color == 'B' or color == 'G' or color == 'Y' or color == 'P':
                if color == player_colors[0]:
                    print "Please pick a different color from player 1."
                else:
                    player_colors.append(color)
                    break
            else:
                print "Please type a valid color symbol. Don't forget to wrap in quotes!"
        except Exception:
            print "Please type a valid color symbol. Don't forget to wrap in quotes!"
    curr_player = 1 if random.random() < .5 else 2
    print
    print player_names[curr_player-1] + " was randomly picked to play first!"
    board = [[tokens[0] for i in range(size)] for j in range(size)]
    for t1 in [-1,0,1]: #list possible neighbors, do this once
        for t2 in [-1,0,1]:
            if t1 != 0 or t2 != 0:
                possible_transitions.append((t1,t2))
    print
    try:
        print "Game is now ready to launch, press enter to begin."
        typed = input()
    except Exception:
        pass

def display_board():
    ''' print the board to the terminal '''
    global board
    print
    for i in range(size):
        print i+1,
        print " ",
    print
    for row in board:
        for elt in row:
            if elt[0] == tokens[1]:
                color_print(0, elt[0])
            elif elt[0] == tokens[2]:
                color_print(1, elt[0])
            else:
                print elt[0],
            print " ",
        print
    print

def get_move():
    ''' ask player which column they would like to move to '''
    global board, size
    print player_names[curr_player-1] + ' it\'s your turn.'
    while True:
        try:
            print "Which column? ",
            col_selected = input() - 1
            if col_selected < 0 or col_selected > size-1:
                print "Invalid move, try again please."
            elif board[0][col_selected] != tokens[0]:
                print "Invalid move, try again please."
            else:
                break
        except Exception:
            print "Invalid move, try again please."
    return col_selected

def move():
    ''' call get_move, then add a players symbol to that column at the
        lowest possible row available. Return values as follows:
        0 : neither player has won, and there are still empty cells
        1 : player1 won the game
        2 : player2 won the game
        3 : tie, all cells filled '''
    global board, size, curr_player, moves_played
    col_selected = get_move()
    row_options = range(size)
    row_options.reverse()
    for row_option in row_options:
        if board[row_option][col_selected] == tokens[0]:
            if curr_player == 1:
                board[row_option][col_selected] = tokens[curr_player]
                if check_endgame(row_option,col_selected):
                    return 1
            elif curr_player == 2:
                board[row_option][col_selected] = tokens[curr_player]
                if check_endgame(row_option,col_selected):
                    return 2
            break
        else:
            pass
    moves_played += 1
    if moves_played >= size * size:
        return 3
    else:
        curr_player = 1 if curr_player == 2 else 2
        return 0

def in_range(row_num, col_num):
    ''' check to see if a row and col pair are inside of the board '''
    if 0 <= row_num < size and 0 <= col_num < size:
        return True
    else:
        return False

def check_endgame(curr_row, curr_col):
    ''' check to see if the games is over, returns true if player who moved
        last won the game, else returns false. Input is the row and column
        selected by the player's most recent move (a win must involve this
        tile)'''
    global board, curr_player, tokens, possible_transitions
    curr_token = tokens[curr_player]
    for t1,t2 in possible_transitions:
        if in_range(curr_row+t1, curr_col+t2) and board[curr_row+t1][curr_col+t2] == curr_token:
            if in_range(curr_row+2*t1,curr_col+2*t2) and board[curr_row+2*t1][curr_col+2*t2] == curr_token:
                if in_range(curr_row+3*t1,curr_col+3*t2) and board[curr_row+3*t1][curr_col+3*t2] == curr_token:
                    return True
                elif in_range(curr_row-t1,curr_col-t2) and board[curr_row-t1][curr_col-t2] == curr_token:
                    return True
            elif in_range(curr_row-t1,curr_col-t2) and board[curr_row-t1][curr_col-t2] == curr_token:
                if in_range(curr_row-2*t1,curr_col-2*t2) and board[curr_row-2*t1][curr_col-2*t2] == curr_token:
                    return True
    return False

def endgame(verdict):
    ''' ends game with following possible inputs -
        1 : player1 won the game
        2 : player2 won the game
        3 : tie, all cells have been filled '''
    if verdict == 1 or verdict == 2:
        print '\n\n\n\n\n'
        winning_statement = '!!' + player_names[verdict-1].upper() + ' WINS!!'
        color_print(verdict-1, winning_statement)
        print '\n\n\n\n\n'
    elif verdict == 3:
        print '\n\n\n\n\n'
        print 'TIED GAME - ALL CELLS ARE FULL!'
        print '\n\n\n\n\n'

if __name__ == '__main__':
    initialize_game()
    verdict = 0
    while True:
        display_board()
        verdict = move()
        if verdict != 0:
            break
    display_board()
    endgame(verdict)
