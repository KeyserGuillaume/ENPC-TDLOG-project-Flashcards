# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QShortcut
from view.games import gameWindow
from model import database, flashcard
from view import AccessSettings, parcours
from numpy.random import shuffle

from random import randrange



class PointToCardGame(gameWindow.GameWindow):
    def __init__(self, parentWindow, cardsPlayed):
        self.parentWindow = parentWindow
        self.cartesJouables = cardsPlayed
        self.nextDisplay = "abort"
    redirect=QtCore.pyqtSignal()
    def stealTheLimelight(self):
        self.allotedTime = AccessSettings.getGameSettings("pointto", 1)
        self.nbSuccessRequired = AccessSettings.getGameSettings("pointto", 0)
        self.nbOfSuggestions = 6
        super().__init__(self.parentWindow, self.nbSuccessRequired, self.allotedTime)
        self.VLayout = QVBoxLayout(self.gameArea)
        self.viewWidget = QLabel(self.gameArea)
        self.viewWidget.setAlignment(QtCore.Qt.AlignCenter)
        self.viewWidget.resize(self.gameArea.frameSize().width(), self.gameArea.frameSize().height()-140)
        self.VLayout.addWidget(self.viewWidget)
        self.resetSignal.connect(self.reset)
        self.newSignal.connect(self.new)
        self.chooseCards()
        self.bottomWidget = QWidget(self.gameArea)
        self.initGame()
        self.show()
    def chooseCards(self):
        languages = database.giveAllLanguages()
        if self.cartesJouables in languages:
            self.cartesJouables = database.getAllCards(self.cartesJouables)
        if self.nbSuccessRequired > len(self.cartesJouables):
            self.nbSuccessRequired = len(self.cartesJouables)
        self.cartesJouees=[]
        while (len(self.cartesJouees) < self.nbSuccessRequired):
            i = randrange(0, len(self.cartesJouables))
            if self.cartesJouables[i] not in self.cartesJouees and self.cartesJouables[i].image != "":
                j = randrange(0, 13)
                if self.cartesJouables[i].level < j:
                    self.cartesJouees.append(self.cartesJouables[i])
        self.nextDisplay = parcours.CardsOverview(self.parentWindow, self.cartesJouees)
    def getPixmap(self, path):
        pixmap = QtGui.QPixmap()
        pixmap.load(path)
        pixmap = pixmap.scaled(self.viewWidget.frameSize().width(),
                               self.viewWidget.frameSize().height(),
                               QtCore.Qt.KeepAspectRatio)
        return pixmap
    def checkAnswer(self, language, word):
        if (word == self.currentCard.word):
            self.onSuccess()
        else:
            self.onFailure(word)
    #initialization for each word
    def initDisplay(self):
        self.viewWidget.setPixmap(self.pixmaps[self.currentCardIndex])
        self.bottomWidget.close()
        randomCards = [database.getRandomCard(self.language) for i in range(self.nbOfSuggestions - 1)]
        randomCards.append(self.currentCard)
        shuffle(randomCards)
        self.bottomWidget = QWidget(self.gameArea)
        HLayout = QHBoxLayout(self.bottomWidget)
        self.choices = [parcours.CardButton(card, self.bottomWidget, self.gameArea.frameSize().width()/(self.nbOfSuggestions + 1), show_native = True) for card in randomCards]
        [HLayout.addWidget(choice) for choice in self.choices]
        self.VLayout.addWidget(self.bottomWidget)
        [choice.openCardSignal.connect(self.checkAnswer) for choice in self.choices]
    def onFailure(self, word):
        self.incrementErrorCount()
        [choice.setText("Wrong") for choice in self.choices if choice.lacarte.word==word ]
    def onSuccess(self):
        self.incrementSuccessCount()
        if self.nbSucces>=self.nbSuccessRequired:
            return
        self.currentCardIndex+=1
        self.currentCard = self.cartesJouees[self.currentCardIndex]
        self.initDisplay()
    def timeIsOut(self):
        super().timeIsOut()
    def gameWon(self):
        super().gameWon()
    def initGame(self):
        super().initGame()
        self.language = self.cartesJouees[0].tablename
        self.pixmaps = [self.getPixmap(card.image) for card in self.cartesJouees]
        self.currentCardIndex = 0
        self.currentCard = self.cartesJouees[0]
        self.initDisplay()
    def clean(self):
        super().clean()
    def reset(self):
        self.clean()
        self.initGame()
    def new(self):
        self.chooseCards()
        self.reset()
