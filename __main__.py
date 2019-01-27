from PyQt5 import QtWidgets
from PyQt5.QtCore import *

from model.AIThread import aiThread
from model.gra import Gra
from model.monoHeurGenerator import MonoHeurGenerator
from model.monteCarloGenerator import MonteCarloGenerator
from view.viewcontroler import Game2048


class GameController:

    def __init__(self, game):
        self.view = None
        self.game = game
        self.remote_control = False
        self.remote_controller = None
        self.threadpool = QThreadPool()
        self.worker = None

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
        self.remote_control = True
        if controller == "stop":
            self.remote_control = False
            if self.worker:
                self.worker.autoDelete()
            return
        self.remote_controller = controller
        self.worker = aiThread(self, steps)
        self.threadpool.start(self.worker)

    def remote_move(self, steps=100):
        if self.remote_control:
            if self.remote_controler == "monteCarlo":
                next_move = MonteCarloGenerator.generateNext(self.game, steps)
            if self.remote_controler == "monoHeur":
                next_move = monoHeurGenerator.generateNext(self.game)
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
    MODE = "REMOTE_HEUR"
    size = 4
    STEPS_NUMBER = 125
    app = QtWidgets.QApplication([])
    nowaGra = Gra(size)
    gameController = GameController(nowaGra)
    if MODE == "NOT_REMOTE":
        g = Game2048(None, gameController, 340, size)
        gameController.setView(g)
        g.move(0, 0)
        g.resize(600, 600)
        # g.changeGridSize(3)
        g.setWindowTitle('2048 Game')
        g.updateTiles()
        g.show()
        app.exec_()
    elif MODE == "MONTE":
        import csv

        for _ in range(89):
            gameController.take_control("monteCarlo", steps=STEPS_NUMBER)
            while gameController.remote_control:
                pass
            score = gameController.score()
            print("Score: ", score)
            print("Highest tile: ", gameController.highestTile())
            with open('statistics/data/monte_carlo_{}_steps.csv'.format(STEPS_NUMBER), 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([gameController.highestTile()])
            gameController.reset_game()
    elif MODE == "REMOTE_HEUR":
        import csv

        for _ in range(100):
            while gameController.game.notOver():
                next_move = MonoHeurGenerator.generateNext(gameController)
                movements = {1: "down", 3: "right", 2: "left", 0: "up"}
                moved, notOver = gameController.move(movements.get(next_move))
                if moved:
                    print(movements.get(next_move))
                    score = gameController.score()
                    print("Score: ", score)
                if not notOver:
                    break
            score = gameController.score()
            print("Score: ", score)
            print("Highest tile: ", gameController.highestTile())
            with open('statistics/data/monte_heur_corner.csv', 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([gameController.highestTile()])
            gameController.reset_game()
