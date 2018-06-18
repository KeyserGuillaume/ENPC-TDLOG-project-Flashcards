# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
import sys
from model import database
from view.games import gameWindow
from random import randrange
from view import AccessSettings


## change la maitrise dans la carte et la base
def modifyLevel(card, upgrade):
    if upgrade == 0:
        return
    card._level += upgrade
    if card._level < 0:
        card._level = 0
    if card._level > 10:
        card._level = 10
    database.modifyCard(card.tablename, card.name, card.trad, card.exemple, card.thema, card.howhard, card.level, card.image, card.pronounciation, card.nature)

### la classe de bouton qui se drop
class ButtonToDrag(QPushButton):
    def __init__(self, card, myType, place, depotLayout):
        self.lacarte=card
        self.language=card.tablename
        self.levelModification = -1
        self.myType=myType
        if myType=='mot':
            super(ButtonToDrag, self).__init__(card.word, place)
        else: #pour l'instant que 2 types donc trad
            super(ButtonToDrag, self).__init__(card.trad, place)
            self.setStyleSheet("background-color: rgb(122, 227, 255);\n" "border-color: rgb(0, 0, 0);\n" "font: 75 13pt \"Helvetica Neue\";")
        self.setAcceptDrops(True)
        self.doneLayout=depotLayout
    error=QtCore.pyqtSignal()
    success=QtCore.pyqtSignal()

    # event on veut bouger la carte
    def mouseMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        text=self.text()+';'+('%d,%d' % (event.x(), event.y()))
        mimeData.setText(text)
        #make a transparent button be dragged by the pointer
        b=QtCore.QCoreApplication.instance ()
        pixmap = QtGui.QScreen.grabWindow(b.primaryScreen(),self.winId())
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.MoveAction)

    # event on a bougé la carte sur une autre carte
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            cardSource = event.source()
            # bouge les 2 cartes dans le layout sur le cote si elles coincident
            if self.text()=="GAME OVER" or self.text()=="TIME IS OUT" or self.myType==cardSource.myType:
                event.ignore()
                event.source().setDown(False)
                return
            if database.match(cardSource.text(),self.text(), self.language) or database.match(self.text(),cardSource.text(), self.language) :
                event.acceptProposedAction()            
                self.success.emit()
                horizontalLayout = QHBoxLayout()
                horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
                horizontalLayout.addWidget(cardSource)
                horizontalLayout.addWidget(self)
                self.doneLayout.addLayout(horizontalLayout)
                self.show()
                cardSource.show()
                event.accept()
                self.levelModification+=4
                #modifyLevel(self.lacarte, +2)
            else:
                # mise a jour de la maitrise des cartes
                # mise a jour du decompte d'erreurs
                self.error.emit()
                event.ignore()
                self.levelModification-=5
                cardSource.levelModification-=5
                #modifyLevel(self.lacarte, -5)
                #modifyLevel(cardSource.lacarte, -5)
        else:
            event.ignore()

class DragAndDropGame(gameWindow.GameWindow):
    def __init__(self, parentWindow, cardsPlayed):
        self.parentWindow = parentWindow
        self.cartesJouables = cardsPlayed
        self.nextDisplay = "abort"
    redirect = QtCore.pyqtSignal()
    def stealTheLimelight(self):
        self.allotedTime = AccessSettings.getGameSettings("dragdrop", 1)
        self.nbSuccessRequired = AccessSettings.getGameSettings("dragdrop", 0)
        super().__init__(self.parentWindow, self.nbSuccessRequired, self.allotedTime)
        self.width = self.gameArea.frameSize().width()
        self.height = self.gameArea.frameSize().height()
        #self.gameArea.setAcceptDrops(True)
        self.setAcceptDrops(True)
        if self.cartesJouees is None:
            self.chooseCards()
        self.initGame()
        self.resetSignal.connect(self.reset)
        self.newSignal.connect(self.new)
    def initGame(self):
        super().initGame()
        ## le layout pour mettre les cartes jouees
        self.doneWidget = QWidget(self.gameArea)
        self.doneWidget.setGeometry(QtCore.QRect(3/4*self.width-10, 10, 1/4*self.width, self.height))
        self.doneLayout = QVBoxLayout(self.doneWidget)
        self.doneLayout.setAlignment(QtCore.Qt.AlignTop)
        self.doneWidget.show()
        ## les futures listes de boutons
        self.myCards = []
        self.myTrads = []
        ## l'ajout de tous les boutons concernes
        for i,carte in enumerate(self.cartesJouees) :
            self.myCards.append(ButtonToDrag(carte,'mot', self, self.doneLayout))
            myx=randrange(5, int(3/4*self.width-150), 1)
            myy=randrange(5, int(3/4*self.height), 1)
            self.myCards[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myCards[i].error.connect(self.incrementErrorCount)
            self.myCards[i].success.connect(self.incrementSuccessCount)
            self.myCards[i].show()
            self.myTrads.append(ButtonToDrag(carte,'trad', self, self.doneLayout))
            myx=randrange(5, int(3/4*self.width-115), 1)
            myy=randrange(5, int(3/4*self.height), 1)
            self.myTrads[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myTrads[i].error.connect(self.incrementErrorCount)
            self.myTrads[i].success.connect(self.incrementSuccessCount)
            self.myTrads[i].show()
        self.show()
    def clean(self):
        super().clean()
        if self.timeLeft > 25:
            bonus = 2 # le jeu a ete remporte avec une grande aisance
        else:
            bonus = 1
        if self.timeLeft > 0 and self.nbSucces < self.nbSuccessRequired:
            bonus = 0 # le jeu n'a pas ete fini
        for i in range(self.nbSuccessRequired):
            modifyLevel(self.cartesJouees[i], bonus * (self.myCards[i].levelModification + self.myTrads[i].levelModification))
            self.myCards[i].close()
            self.myTrads[i].close()
        self.doneWidget.close()
    def reset(self):
        self.clean()
        self.initGame()
    def new(self):
        self.chooseCards()
        self.reset()
    def timeIsOut(self):
        super().timeIsOut()
        for carte in self.myCards:
            carte.setText('TIME IS OUT')
        for carte in self.myTrads:
            carte.setText('GAME OVER')
    def dragEnterEvent(self, e):
        e.accept()
    def dropEvent(self, e):
        mime = e.mimeData().text()
        mime = (mime.split(';'))[1]
        x, y = map(int, mime.split(','))
        e.source().move(e.pos()-QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        e.source().setDown(False)
            
            
            
            
            