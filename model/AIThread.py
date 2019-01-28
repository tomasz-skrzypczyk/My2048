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
        while self.gameController.remote_control and self.gameController.game.notOver():
            self.gameController.remote_move(self.steps)
        self.gameController.remote_control = False
        self.gameController.remoteOff()
        # if not self.gameController.game.notOver():
        #     self.gameController.gameOver()
