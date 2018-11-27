#!/usr/bin/python
from PyQt5 import QtCore,QtGui, QtWidgets
import random
from view.tile import Tile



class Game2048(QtWidgets.QWidget):
	def __init__(self,parent, gameController,width=340,gridSize=4):
		QtWidgets.QWidget.__init__(self,parent)
		self.gameController = gameController
		self.gameRunning=False
		self.panelHeight=80
		self.backgroundBrush=QtGui.QBrush(QtGui.QColor(0xbbada0))
		self.gridSize=gridSize
		self.tileMargin=16
		self.gridOffsetX=self.tileMargin
		self.gridOffsetY=self.panelHeight+self.tileMargin
		self.brushes={
			0:QtGui.QBrush(QtGui.QColor(0xcdc1b4)),
			1:QtGui.QBrush(QtGui.QColor(0x999999)),
			2:QtGui.QBrush(QtGui.QColor(0xeee4da)),
			4:QtGui.QBrush(QtGui.QColor(0xede0c8)),
			8:QtGui.QBrush(QtGui.QColor(0xf2b179)),
			16:QtGui.QBrush(QtGui.QColor(0xf59563)),
			32:QtGui.QBrush(QtGui.QColor(0xf67c5f)),
			64:QtGui.QBrush(QtGui.QColor(0xf65e3b)),
			128:QtGui.QBrush(QtGui.QColor(0xedcf72)),
			256:QtGui.QBrush(QtGui.QColor(0xedcc61)),
			512:QtGui.QBrush(QtGui.QColor(0xedc850)),
			1024:QtGui.QBrush(QtGui.QColor(0xedc53f)),
			2048:QtGui.QBrush(QtGui.QColor(0xedc22e)),
		}
		self.lightPen=QtGui.QPen(QtGui.QColor(0xf9f6f2))
		self.darkPen=QtGui.QPen(QtGui.QColor(0x776e65))
		self.scoreRect=QtCore.QRect(10,10,80,self.panelHeight-20)
		self.hiScoreRect=QtCore.QRect(100,10,80,self.panelHeight-20)
		self.resetRect=QtCore.QRectF(190,10,80,self.panelHeight-20)
		self.scoreLabel=QtCore.QRectF(10,25,80,self.panelHeight-30)
		self.hiScoreLabel=QtCore.QRectF(100,25,80,self.panelHeight-30)
		self.hiScore=0
		self.lastPoint=None
		self.resize(QtCore.QSize(width,width+self.panelHeight))
		self.reset_game()

	def resizeEvent(self,e):
		width=min(e.size().width(),e.size().height()-self.panelHeight)
		self.tileSize=(width-self.tileMargin*(self.gridSize+1))/self.gridSize
		self.font=QtGui.QFont('Arial',self.tileSize/4)

	def changeGridSize(self,x):
		self.gridSize=x
		self.reset_game()

	def reset_game(self):
        #do usuniecia
		self.tiles=[[None for i in range(0,self.gridSize)] for i in range(0,self.gridSize)]
        #self.tiles = main.reset_game()
        #do usuniecia
		self.availableSpots=list(range(0,self.gridSize*self.gridSize))
		self.score=0
        #do suniecia


		self.update()
		self.gameRunning=True


	def up(self):
		moved = self.gameController.move("up")
		if moved:
			self.updateTiles()

	def down(self):
		moved=self.gameController.move("down")
		if moved:
			self.updateTiles()

	def left(self):
		moved = self.gameController.move("left")
		if moved:
			self.updateTiles()

	def right(self):
		moved = self.gameController.move("right")
		if moved:
			self.updateTiles()

	def updateTiles(self):
        #do usuniecia
		self.availableSpots=[]
		for i in range(0,self.gridSize):
			for j in range(0,self.gridSize):
				if self.tiles[i][j] is None:
					self.availableSpots.append(i+j*self.gridSize)

		self.hiScore=max(self.score,self.hiScore)
		self.update()
		if not self.movesAvailable():
			QtGui.QMessageBox.information(self,'','Game Over')
			self.gameRunning=False

	def movesAvailable(self):
		if not len(self.availableSpots)==0:
			return True
		for i in range(0,self.gridSize):
			for j in range(0,self.gridSize):
				if i<self.gridSize-1 and self.tiles[i][j].value==self.tiles[i+1][j].value:
					return True
				if j<self.gridSize-1 and self.tiles[i][j].value==self.tiles[i][j+1].value:
					return True
		return False

	def keyPressEvent(self,e):
		if not self.gameRunning:
			return
		if e.key()==QtCore.Qt.Key_Escape:
			self.reset_game()
		elif e.key()==QtCore.Qt.Key_Up:
			self.up()
		elif e.key()==QtCore.Qt.Key_Down:
			self.down()
		elif e.key()==QtCore.Qt.Key_Left:
			self.left()
		elif e.key()==QtCore.Qt.Key_Right:
			self.right()

	def mousePressEvent(self,e):
		self.lastPoint=e.pos()

	def mouseReleaseEvent(self,e):
		if self.resetRect.contains(self.lastPoint.x(),self.lastPoint.y()) and self.resetRect.contains(e.pos().x(),e.pos().y()):
			if QtGui.QMessageBox.question(self,'','Are you sure you want to start a new game?',
					QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)==QtGui.QMessageBox.Yes:
				self.reset_game()
		elif self.gameRunning and self.lastPoint is not None:
			dx=e.pos().x()-self.lastPoint.x()
			dy=e.pos().y()-self.lastPoint.y()
			if abs(dx)>abs(dy) and abs(dx)>10:
				if dx>0:
					self.right()
				else:
					self.left()
			elif abs(dy)>10:
				if dy>0:
					self.down()
				else:
					self.up()


	def paintEvent(self,event):
		painter = QtGui.QPainter(self)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(self.backgroundBrush)
		painter.drawRect(self.rect())
		painter.setBrush(self.brushes[1])
		painter.drawRoundedRect(self.scoreRect,10.0,10.0)
		painter.drawRoundedRect(self.hiScoreRect,10.0,10.0)
		painter.drawRoundedRect(self.resetRect,10.0,10.0)
		painter.setFont(QtGui.QFont('Arial',9))
		painter.setPen(self.darkPen)
		painter.drawText(QtCore.QRectF(10,15,80,20),'SCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.drawText(QtCore.QRectF(100,15,80,20),'HIGHSCORE',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.setFont(QtGui.QFont('Arial',15))
		painter.setPen(self.lightPen)
		painter.drawText(self.resetRect,'RESET',QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.setFont(QtGui.QFont('Arial',15))
		painter.setPen(self.lightPen)
		painter.drawText(self.scoreLabel,str(self.score),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.drawText(self.hiScoreLabel,str(self.hiScore),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.setFont(self.font)
		for gridX in range(0,self.gridSize):
			for gridY in range(0,self.gridSize):
				tile = self.tiles[gridX][gridY]
				if tile is None:
					painter.setBrush(self.brushes[0])
				else:
					painter.setBrush(self.brushes[tile.value])
				rect=QtCore.QRectF(self.gridOffsetX+gridX*(self.tileSize+self.tileMargin),
										self.gridOffsetY+gridY*(self.tileSize+self.tileMargin),
										self.tileSize,self.tileSize)
				painter.setPen(QtCore.Qt.NoPen)
				painter.drawRoundedRect(rect,10.0,10.0)
				if tile is not None:
					painter.setPen(self.darkPen if tile.value<16 else self.lightPen)
					painter.drawText(rect,str(tile.value),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))


