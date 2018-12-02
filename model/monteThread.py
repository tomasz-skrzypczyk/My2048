from PyQt5.QtCore import *


class monteThread(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self, game):
        super(monteThread, self).__init__()
        self.game = game

    @pyqtSlot()
    def run(self):
        while self.game.remote_controle == True:
            self.game.remote_move()
