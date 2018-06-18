# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QPushButton
from view.games import gameWindow
from view import AccessSettings
from math import ceil
from random import shuffle

class PlayingCard(QPushButton):
    def __init__(self, index, myType, place):
        super(PlayingCard, self).__init__(place)
        self.index = index
        self.nature = myType # carte de mot (0) ou de trad (1)
        self.face = 0 # 0 si cote cache, 1 si cote ecrit, 2 si deja en paire
        self.setMinimumSize(QtCore.QSize(100, 80))
        self.setMaximumSize(QtCore.QSize(100, 80))
        self.setStyleSheet("background-image: url(:/fond/green.jpg);\n" "font: 87 13pt \"Arial Black\";")
        self.clicked.connect(lambda x:self.flipSignal.emit(self.index, self.nature, self.face))
    flipSignal=QtCore.pyqtSignal(int, int, int)

class MemoryGame(gameWindow.GameWindow):
    def __init__(self, parentWindow, cardsPlayed):
        self.parentWindow=parentWindow
        self.cartesJouables=cardsPlayed
        self.nextDisplay="abort"
    redirect=QtCore.pyqtSignal()
    def stealTheLimelight(self):
        self.allotedTime = AccessSettings.getGameSettings("memory", 1)
        self.nbSuccessRequired = AccessSettings.getGameSettings("memory", 0)
        super().__init__(self.parentWindow, self.nbSuccessRequired, self.allotedTime)
        self.scrollableGameArea=QScrollArea(self.gameArea)
        self.scrollableGameArea.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.scrollableGameArea.setWidgetResizable(True)
        self.scrollableGameArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollableGameArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        self.resetSignal.connect(self.reset)
        self.newSignal.connect(self.new)
        self.chooseCards()
        self.initGame()
        self.show()
    def initGame(self):
        super().initGame()
        self.plateau = QWidget(self.scrollableGameArea)
        self.plateau.setGeometry(QtCore.QRect(20, 20, 670, 120*ceil(2*self.nbSuccessRequired/5)))
        self.plateau.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.gridLayout = QGridLayout(self.plateau)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)        
        # creation des cartes de jeu a raison de 2 par flashcard en jeu
        self.cardWidgets = [None]*2*self.nbSuccessRequired
        shuffle(self.cartesJouees)
        self.permutation=list(range(0, 2*self.nbSuccessRequired))
        shuffle(self.permutation)
        for i in range(self.nbSuccessRequired):
            self.cardWidgets[self.permutation[2*i]] = PlayingCard(2*i, 0, self.plateau)
            self.cardWidgets[self.permutation[2*i+1]] = PlayingCard(2*i+1, 1, self.plateau)
        for i in range(len(self.cardWidgets)):
            # 5 cartes par ligne
            row = i // 5
            column = i % 5
            self.gridLayout.addWidget(self.cardWidgets[i], row, column, 1, 1)
            self.cardWidgets[i].flipSignal.connect(self.flip)
        self.scrollableGameArea.setWidget(self.plateau)
        self.yellowCards=[]
    def flip(self, index, nature, face):
        if self.timeLeft < 0:
            return
        current = len(self.yellowCards)
        # changement de cote de la carte
        if face == 0 and current < 2:
            self.cardWidgets[self.permutation[index]].setStyleSheet("background-image: url(:/fond/yellow.jpg);\n" "font: 87 13pt \"Arial Black\";")
            current += 1
            if nature == 0:
                self.cardWidgets[self.permutation[index]].setText(self.cartesJouees[index//2].word)
            else:
                self.cardWidgets[self.permutation[index]].setText(self.cartesJouees[index//2].trad)
            self.cardWidgets[self.permutation[index]].face = 1
            self.yellowCards.append(self.cardWidgets[self.permutation[index]])
        elif face == 1 and current>0:
            self.cardWidgets[self.permutation[index]].setStyleSheet("background-image: url(:/fond/green.jpg);\n" "font: 87 13pt \"Arial Black\";")
            self.cardWidgets[self.permutation[index]].setText(" ")
            self.face = 0
            current-=1
            self.yellowCards.remove(self.cardWidgets[self.permutation[index]])
            self.cardWidgets[self.permutation[index]].face = 0
        ## gere le cas de deja en paire :
        if self.matchingCards():
            for matchedcard in self.yellowCards :
                matchedcard.setStyleSheet("background-image: url(:/fond/silver.jpg);\n" "font: 87 13pt \"Arial Black\";")
                matchedcard.laface = 2
                matchedcard.setEnabled(False)
            self.yellowCards = []
            self.incrementSuccessCount()
    def matchingCards(self):
    #si 2 carte retournees
        if len(self.yellowCards)==2 and self.yellowCards[0].index//2 == self.yellowCards[1].index//2:
            return True
        else:
            return False
    def clean(self):
        super().clean()
        self.plateau.close()
    def reset(self):
        self.clean()
        self.initGame()
    def new(self):
        self.chooseCards()
        self.reset()