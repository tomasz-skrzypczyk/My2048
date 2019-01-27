from PyQt5.QtCore import *


class aiThread(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, gameController, steps=100):
        super(aiThread, self).__init__()
        self.gameController = gameController
        self.steps = steps

    @pyqtSlot()
    def run(self):
        while self.gameController.remote_controle and self.gameController.game.notOver():
            self.gameController.remote_move(self.steps)
        self.gameController.remote_controle = False
        self.gameController.gameOver()
