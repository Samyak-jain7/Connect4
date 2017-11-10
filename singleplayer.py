from connect4 import Game
from ai import MiniMax

'''
##### PARAMETERS #####
reward_connections : bool tovalue states where 4 token connections are possible
min_think_time : minimum time ai will think (then abort after finishing iteration)
min_depth : minimum depth ai will search regardless of time
discount : exponential decay penalty for rewards over time
'''
reward_connections = True
min_think_time = 3
min_depth = 3
discount = .1

if __name__ == '__main__':
    game = Game(ai_bool=True)
    game.setup()
    ai_agent = MiniMax(tokens = game.tokens, \
                       possible_transitions = game.possible_transitions, \
                       size = game.size, \
                       reward_connections = reward_connections, \
                       min_think_time = min_think_time, \
                       min_depth = min_depth, \
                       discount = discount)
    verdict = 0
    while verdict==0:
        game.displayBoard()
        if game.curr_player == 1:
            verdict = game.move()
        else:
            print "%s is thinking..." % game.player_names[1]
            v, a, d = ai_agent.pickColumn(board = game.board, \
                                          moves_played = game.moves_played)
            print "...%i moves ahead" % (2*d)
            verdict = game.move(ai_in=a)
    game.displayBoard()
    game.endGame(verdict)
