from connect4 import Game
from ai import MiniMax
import random

if __name__ == '__main__':
    game = Game(ai_bool=True)
    game.setup()
    ai_agent = MiniMax(tokens = game.tokens,\
                       possible_transitions = game.possible_transitions,\
                       size = game.size)
    verdict = 0
    while verdict==0:
        game.displayBoard()
        if game.curr_player == 1:
            verdict = game.move()
        else:
            print "%s is thinking..." % game.player_names[1]
            v, a = ai_agent.pickColumn(game.board, game.moves_played)
            verdict = game.move(ai_in=a)
    game.displayBoard()
    game.endGame(verdict)
