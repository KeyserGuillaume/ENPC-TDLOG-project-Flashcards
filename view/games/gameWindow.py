# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel
import sys
from model import database
from random import randrange
from view import parcours

from time import time, strftime,localtime

#nbSuccessRequired defines how many good answers you need to get before winning
class GameWindow (QWidget):
    def __init__(self, parentWindow, nbSuccessRequired, chosenChrono):
        """
        The common component of all games
        parentWindow : the widget in which this window is displayed
        nbSuccessRequired : the nb of successes required for clearing the game
        chosenChrono : the time available to clear the game
        """
        super(QWidget, self).__init__(parentWindow)
        self.timeGiven = chosenChrono
        self.nbSuccessRequired = nbSuccessRequired
        self.cartesJouees = None
        self.setWindowTitle("Drag and Drop")
        self.resize(self.parent().frameSize())# le jeu comme defini ci dessus
        self.layout=QVBoxLayout(self)
        self.gameArea=QWidget(self)
        self.gameArea.setFixedSize(self.frameSize().width(), self.frameSize().height()-65)
        self.layout.addWidget(self.gameArea)
        ## la barre de boutons/compteurs du bas
        self.BottomWidget = QWidget(self)
        self.BottomWidget.resize(self.frameSize().width()-20, 61)
        self.layout.addWidget(self.BottomWidget)
        self.GameBox = QHBoxLayout(self.BottomWidget)
        self.GameBox.setContentsMargins(0, 0, 0, 0)
        # les boutons de gestion de partie
        self.viewButton = QPushButton(u"View Cards", self.BottomWidget)
        self.viewButton.clicked.connect(self.redirect.emit)
        self.GameBox.addWidget(self.viewButton)
        self.resetButton = QPushButton(u"Reset",self.BottomWidget)
        self.resetButton.clicked.connect(self.resetSignal.emit)
        self.GameBox.addWidget(self.resetButton)
        self.newButton = QPushButton(u"New Round",self.BottomWidget)
        self.newButton.clicked.connect(self.newSignal.emit)
        self.GameBox.addWidget(self.newButton)
        # compteur chrono
        self.chrono = QLCDNumber(self.BottomWidget)
        self.chrono.setDigitCount(2)
        self.GameBox.addWidget(self.chrono)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.nberreurs=0
        self.nbSucces=0        
        self.t0=time()
        # bouton pour afficher ses erreurs
        self.mistakesButton = QPushButton("See mistakes",self.BottomWidget)
        self.GameBox.addWidget(self.mistakesButton)
        self.mistakesButton.setEnabled(False)
        # compteur d'erreurs
        self.failure = QLCDNumber(self.BottomWidget)
        self.failure.setStyleSheet("color: rgb(252, 0, 6);\n" "border-color: rgb(0, 0, 0);\n" "")
        self.failure.setDigitCount(5)
        self.GameBox.addWidget(self.failure)
        #le message de victoire
        self.victoryButton = QPushButton(self)
        self.victoryButton.setGeometry(QtCore.QRect(230, 130, 251, 221))
        self.victoryButton.setStyleSheet("background-image: url(:/icons/win.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.victoryButton.setVisible(False)
        qr=self.victoryButton.frameGeometry()
        qr.moveCenter(self.gameArea.rect().center())
        self.victoryButton.move(qr.topLeft())
        # le message de defaite
        self.defeatButton = QPushButton(self)
        self.defeatButton.setGeometry(QtCore.QRect(230, 130, 221, 221))
        self.defeatButton.setStyleSheet(
            "background-image: url(:/icons/gameover2.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.defeatButton.setVisible(False)
        qr=self.defeatButton.frameGeometry()
        qr.moveCenter(self.gameArea.rect().center())
        self.defeatButton.move(qr.topLeft())
        
        self.mistakesButton.setEnabled(False)        
        
    resetSignal = QtCore.pyqtSignal()
    newSignal = QtCore.pyqtSignal()
    viewSignal = QtCore.pyqtSignal()
    redirect = QtCore.pyqtSignal()
        
    def incrementSuccessCount(self):
        self.nbSucces+=1;
        if (self.nbSucces==self.nbSuccessRequired):
            self.gameWon()
    def incrementErrorCount(self):
        self.nberreurs+=1
    def Time(self):
        if self.nbSucces==self.nbSuccessRequired:
            return
        self.timeLeft=self.timeGiven-(time()-self.t0)//1
        if self.timeLeft < 0:
            self.timeIsOut()
            return
        self.chrono.display(self.timeLeft)
        self.failure.display(self.nberreurs)
    def initGame(self):
        self.nberreurs=0
        self.nbSucces=0
        self.t0=time()
        self.timer.start(10)
    def timeIsOut(self):
        self.defeatButton.show()
        self.timer.stop()
    def gameWon(self):
        self.victoryButton.show()
    def clean(self):        
        self.victoryButton.hide()
        self.defeatButton.hide()
    def toTheShadows(self):
        self.clean()
        self.close()
    def chooseCards(self):
        languages = database.giveAllLanguages()
        if self.cartesJouables in languages:
            self.cartesJouables = database.getAllCards(self.cartesJouables)
        if self.nbSuccessRequired > len(self.cartesJouables):
            self.nbSuccessRequired = len(self.cartesJouables)
        self.cartesJouees=[]
        while (len(self.cartesJouees) < self.nbSuccessRequired):
            i=randrange(0, len(self.cartesJouables))
            if self.cartesJouables[i] not in self.cartesJouees:
                j=randrange(0, 13)
                if self.cartesJouables[i].level < j:
                    self.cartesJouees.append(self.cartesJouables[i])
        self.nextDisplay = parcours.CardsOverview(self.parentWindow, self.cartesJouees)