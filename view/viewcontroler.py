#!/usr/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit

from view.tile import Tile


class Game2048(QtWidgets.QWidget):
    def __init__(self, parent, gameController, width=340, gridSize=4):
        QtWidgets.QWidget.__init__(self, parent)
        self.gameController = gameController
        self.tiles = [[None for x in range(0, gridSize)] for y in range(0, gridSize)]
        self.gameRunning = False
        self.GameOver = False
        self.panelHeight = 80
        self.backgroundBrush = QtGui.QBrush(QtGui.QColor(0xbbada0))
        self.gridSize = gridSize
        self.tileMargin = 16
        self.gridOffsetX = self.tileMargin
        self.gridOffsetY = self.panelHeight + self.tileMargin
        self.brushes = {
            0: QtGui.QBrush(QtGui.QColor(0xcdc1b4)),
            1: QtGui.QBrush(QtGui.QColor(0x999999)),
            2: QtGui.QBrush(QtGui.QColor(0xeee4da)),
            4: QtGui.QBrush(QtGui.QColor(0xede0c8)),
            8: QtGui.QBrush(QtGui.QColor(0xf2b179)),
            16: QtGui.QBrush(QtGui.QColor(0xf59563)),
            32: QtGui.QBrush(QtGui.QColor(0xf67c5f)),
            64: QtGui.QBrush(QtGui.QColor(0xf65e3b)),
            128: QtGui.QBrush(QtGui.QColor(0xedcf72)),
            256: QtGui.QBrush(QtGui.QColor(0xedcc61)),
            512: QtGui.QBrush(QtGui.QColor(0xedc850)),
            1024: QtGui.QBrush(QtGui.QColor(0xedc53f)),
            2048: QtGui.QBrush(QtGui.QColor(0xedc22e)),
            4096: QtGui.QBrush(QtGui.QColor(0xedffff)),
            8192: QtGui.QBrush(QtGui.QColor(0xedffff)),
        }
        self.lightPen = QtGui.QPen(QtGui.QColor(0xf9f6f2))
        self.darkPen = QtGui.QPen(QtGui.QColor(0x776e65))
        self.redPen = QtGui.QPen(QtGui.QColor(0x771010))
        self.scoreRect = QtCore.QRect(10, 10, 80, self.panelHeight - 20)
        self.hiScoreRect = QtCore.QRect(100, 10, 80, self.panelHeight - 20)
        self.resetRect = QtCore.QRectF(190, 10, 80, self.panelHeight - 20)

        self.monteCarloRect = QtCore.QRectF(280, 10, 80, self.panelHeight - 20)
        self.monteCarloRemote = False

        self.monoHeurRect = QtCore.QRectF(460, 10, 80, self.panelHeight - 20)
        self.monoHeurRemote = False

        self.line = QLineEdit(self)
        self.line.focusPolicy()
        self.line.setText("100")
        self.scoreLabel = QtCore.QRectF(10, 25, 80, self.panelHeight - 30)
        self.hiScoreLabel = QtCore.QRectF(100, 25, 80, self.panelHeight - 30)
        self.hiScore = 0
        self.score = 0
        self.lastPoint = None
        self.resize(QtCore.QSize(width, width + 2 * self.panelHeight))

    def resizeEvent(self, e):
        width = min(e.size().width(), e.size().height() - self.panelHeight)
        self.tileSize = (width - self.tileMargin * (self.gridSize + 1)) / self.gridSize
        self.font = QtGui.QFont('Arial', self.tileSize / 4)

    def changeGridSize(self, x):
        self.gridSize = x
        self.reset_game()

    def reset_game(self):

        self.gameController.reset_game()
        self.score = 0
        self.tiles = [[Tile(t) if t != -1 else None for t in y] for y in self.gameController.tiles().plansza]
        self.update()
        self.gameRunning = True

    def up(self):
        moved = self.gameController.move("up")
        if moved[0]:
            self.updateTiles()
        if not moved[1]:
            self.gameOver()

    def down(self):
        moved = self.gameController.move("down")
        if moved[0]:
            self.updateTiles()
        if not moved[1]:
            self.gameOver()

    def left(self):
        moved = self.gameController.move("left")
        if moved[0]:
            self.updateTiles()
        if not moved[1]:
            self.gameOver()

    def right(self):
        moved = self.gameController.move("right")
        if moved[0]:
            self.updateTiles()
        if not moved[1]:
            self.gameOver()

    def gameOver(self):
        self.monteCarloRemote = False
        # wszystki remote = False
        QtWidgets.QMessageBox.information(self, '', 'Game Over')
        self.gameRunning = False

    def updateTiles(self):
        # do usuniecia
        self.tiles = [[Tile(t) if t != -1 else None for t in y] for y in self.gameController.tiles().plansza]
        self.score = self.gameController.score()
        self.hiScore = max(self.score, self.hiScore)
        self.gameRunning = True
        self.update()

    def keyPressEvent(self, e):
        if not self.gameRunning:
            return
        if e.key() == QtCore.Qt.Key_Escape:
            self.reset_game()
        elif e.key() == QtCore.Qt.Key_Up:
            self.up()
        elif e.key() == QtCore.Qt.Key_Down:
            self.down()
        elif e.key() == QtCore.Qt.Key_Left:
            self.left()
        elif e.key() == QtCore.Qt.Key_Right:
            self.right()

    def mousePressEvent(self, e):
        self.lastPoint = e.pos()

    def mouseReleaseEvent(self, e):
        if self.resetRect.contains(self.lastPoint.x(), self.lastPoint.y()) and self.resetRect.contains(e.pos().x(),
                                                                                                       e.pos().y()):
            if QtWidgets.QMessageBox.question(self, '', 'Are you sure you want to start a new gameController?',
                                              QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
                self.reset_game()
        elif self.monteCarloRect.contains(self.lastPoint.x(), self.lastPoint.y()) and self.monteCarloRect.contains(
                e.pos().x(),
                e.pos().y()):
            self.monteCarloRemote = False if self.monteCarloRemote is True else True
            if self.line.text().isdigit() is False or int(self.line.text()) < 10:
                self.line.setText("100")
            if self.monteCarloRemote:
                self.gameController.take_control("monteCarlo", steps=int(self.line.text()))
            else:
                self.gameController.take_control("stop")
        elif self.monoHeurRect.contains(self.lastPoint.x(), self.lastPoint.y()) and self.monoHeurRect.contains(
                e.pos().x(),
                e.pos().y()):
            self.monoHeurRemote = False if self.monoHeurRemote is True else True
            if self.monoHeurRemote:
                self.gameController.take_control("monoHeur")
            else:
                self.gameController.take_control("stop")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawRect(self.rect())
        painter.setBrush(self.brushes[1])
        painter.drawRoundedRect(self.scoreRect, 10.0, 10.0)
        painter.drawRoundedRect(self.hiScoreRect, 10.0, 10.0)
        painter.drawRoundedRect(self.resetRect, 10.0, 10.0)
        painter.drawRoundedRect(self.monteCarloRect, 10.0, 10.0)
        painter.drawRoundedRect(self.monoHeurRect, 10.0, 10.0)
        self.line.move(370,
                       10)
        self.line.resize(80, self.panelHeight - 20)
        painter.setFont(QtGui.QFont('Arial', 9))
        painter.setPen(self.darkPen)
        painter.drawText(QtCore.QRectF(10, 15, 80, 20), 'SCORE',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.drawText(QtCore.QRectF(100, 15, 80, 20), 'HIGHSCORE',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        if self.monteCarloRemote is False:
            painter.setPen(self.lightPen)
        else:
            painter.setPen(self.redPen)
        painter.drawText(self.monteCarloRect, 'Monte Carlo AI',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setPen(self.darkPen)
        painter.drawText(self.monoHeurRect, 'Monotonous heuristic AI',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial', 15))
        painter.setPen(self.lightPen)
        painter.drawText(self.resetRect, 'RESET', QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))

        painter.setFont(QtGui.QFont('Arial', 15))
        painter.setPen(self.lightPen)
        painter.drawText(self.scoreLabel, str(self.score),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.drawText(self.hiScoreLabel, str(self.hiScore),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(self.font)
        for gridX in range(0, self.gridSize):
            for gridY in range(0, self.gridSize):
                tile = self.tiles[gridX][gridY]
                if tile is None:
                    painter.setBrush(self.brushes[0])
                else:
                    value = 2 ** tile.value if tile.value != -1 else None
                    painter.setBrush(self.brushes[value])
                rect = QtCore.QRectF(self.gridOffsetX + gridX * (self.tileSize + self.tileMargin),
                                     self.gridOffsetY + gridY * (self.tileSize + self.tileMargin),
                                     self.tileSize, self.tileSize)
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(rect, 10.0, 10.0)
                if tile is not None:
                    painter.setPen(self.darkPen if value < 16 else self.lightPen)
                    painter.drawText(rect, str(value),
                                     QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial', 15))
        painter.setBrush(self.brushes[1])
