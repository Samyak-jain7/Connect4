from connect4 import Game

if __name__ == '__main__':
    game = Game()
    game.setup()
    verdict = 0
    while verdict==0:
        game.displayBoard()
        verdict = game.move()
    game.displayBoard()
    game.endGame(verdict)
