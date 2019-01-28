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
        self.game: Gra = game
        self.remote_control = False
        self.remote_controller = None
        self.threadpool = QThreadPool()
        self.worker = None

    def setView(self, view):
        self.view = view

    def move(self, movement: str):
        notOver = self.game.notOver()
        if notOver:
            if movement in ["up", "down", "left", "right"]:
                movements = {"down": 1, "right": 3, "left": 2, "up": 0}
                moved = self.game.move(movements.get(movement))
                notOver = self.game.notOver()
            else:
                return False, False
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
        if not self.game.notOver():
            return
        self.remote_control = True
        if controller == "stop":
            self.remote_control = False
            if self.worker:
                self.worker.autoDelete()
            return
        self.remote_controler = controller
        self.worker = aiThread(self, steps)
        self.threadpool.start(self.worker)

    def remoteOff(self):
        self.view.remoteOff()

    def remote_move(self, steps=100):
        if self.remote_control:
            if self.remote_controler == "monteCarlo":
                next_move = MonteCarloGenerator.generateNext(self.game, steps)
            if self.remote_controler == "monoHeur":
                next_move = MonoHeurGenerator.generateNext(self.game)
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
    MODE = "NOT_REMOTE"
    SIZE = 4
    STEPS_NUMBER = 75
    app = QtWidgets.QApplication([])
    nowaGra = Gra(SIZE)
    gameController = GameController(nowaGra)
    if MODE == "NOT_REMOTE":
        g = Game2048(None, gameController, 340, SIZE)
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

        for _ in range(1):
            while gameController.game.notOver():
                next_move = MonteCarloGenerator.generateNext(gameController.game, steps=STEPS_NUMBER)
                movements = {1: "down", 3: "right", 2: "left", 0: "up"}
                moved, notOver = gameController.move(movements.get(next_move))
                # if moved:
                #     print(movements.get(next_move))
                #     score = gameController.score()
                #     print("Score: ", score)
                if not notOver:
                    break
            score = gameController.score()
            print("Score: ", score)
            print("Highest tile: ", gameController.highestTile())
            if STEPS_NUMBER < 100:
                filename = 'statistics/data/{}x{}_monte_carlo_0{}_steps.csv'.format(SIZE, SIZE, STEPS_NUMBER)
            else:
                filename = 'statistics/data/{}x{}_monte_carlo_{}_steps.csv'.format(SIZE, SIZE, STEPS_NUMBER)

            with open(filename, 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([gameController.highestTile()])
            gameController.reset_game()

    elif MODE == "REMOTE_HEUR":
        import csv

        DEPTH = 3
        BRANCHING_FACTOR = 6
        for _ in range(10):
            while gameController.game.notOver():
                next_move = MonoHeurGenerator.generateNext(gameController.game, depth=DEPTH,
                                                           branching_factor=BRANCHING_FACTOR)
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
            with open('statistics/data/mono_heur_corner_depth_{}_bf_{}.csv'.format(DEPTH, BRANCHING_FACTOR), 'a',
                      newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([gameController.highestTile()])
            gameController.reset_game()
