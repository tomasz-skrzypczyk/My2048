from PyQt5 import QtWidgets
from PyQt5.QtCore import *

from model.gra import Gra
from model.monteCarloGenerator import MonteCarloGenerator
from model.monteThread import monteThread
from view.viewcontroler import Game2048


class GameController:

    def __init__(self, game):
        self.view = None
        self.game = game
        self.remote_controle = False
        self.remote_controller = None
        self.threadpool = QThreadPool()

    def setView(self, view):
        self.view = view

    def move(self, movement):
        notOver = self.game.notOver()
        if notOver:
            if movement in ["up", "down", "left", "right"]:
                movements = {"down": 1, "right": 3, "left": 2, "up": 0}
                moved = self.game.move(movements.get(movement))
                notOver = self.game.notOver()
            return moved, notOver
        else:
            return False, False

    def reset_game(self):
        self.game = Gra(int(self.game.size))

    def tiles(self):
        return self.game.table

    def score(self):
        return self.game.score

    def highestTile(self):
        return self.game.highestTile()

    def take_control(self, controller, steps=100):
        if not self.remote_controle:
            self.remote_controle = True
        else:
            self.remote_controle = False
        if controller == "monteCarlo":
            self.remote_controller = "monteCarlo"
            worker = monteThread(self, steps)
            self.threadpool.start(worker)

    def remote_move(self, steps=100):
        if self.remote_controle:
            next_move = MonteCarloGenerator.generateNext(self.game, steps)
            movements = {1: "down", 3: "right", 2: "left", 0: "up"}
            moved, notOver = self.move(movements.get(next_move))
            if notOver is False:
                pass
            if self.view:
                self.view.updateTiles()
                self.view.update()
    def gameOver(self):
        if self.view:
            self.view.gameOver()


if __name__ == '__main__':
    MODE = "REMOTE"
    size = 4
    STEPS_NUMBER = 50
    app = QtWidgets.QApplication([])
    nowaGra = Gra(size)
    gameController = GameController(nowaGra)
    if MODE != "REMOTE":
        g = Game2048(None, gameController, 340, size)
        gameController.setView(g)
        g.move(0, 0)
        g.resize(400, 600)
        # g.changeGridSize(3)
        g.setWindowTitle('2048 Game')
        g.updateTiles()
        g.show()
        app.exec_()
    else:
        import csv

        with open('monte_carlo_{}_steps.csv'.format(STEPS_NUMBER), 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for _ in range(80):
                gameController.take_control("monteCarlo", steps = STEPS_NUMBER)
                while gameController.remote_controle:
                    pass
                score = gameController.score()
                print("Score: ", score)
                print("Highest tile: ", gameController.highestTile())
                spamwriter.writerow([gameController.highestTile()])
                gameController.reset_game()


