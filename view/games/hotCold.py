# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QGridLayout, QShortcut
from view.games import gameWindow
from model import database, rechercheFonct, flashcard
from view import AccessSettings, parcours


class HotAndColdGame(gameWindow.GameWindow):
    def __init__(self, parentWindow, cardsPlayed):
        self.parentWindow=parentWindow
        self.cartesJouables=cardsPlayed
        self.nextDisplay="abort"
    redirect=QtCore.pyqtSignal()
    def stealTheLimelight(self):
        self.allotedTime = AccessSettings.getGameSettings("hotcold", 1)
        self.nbSuccessRequired = AccessSettings.getGameSettings("hotcold", 0)
        super().__init__(self.parentWindow, self.nbSuccessRequired, self.allotedTime)
        
        self.layout=QGridLayout(self.gameArea)
        self.gameArea.setStyleSheet("background-image: url(:/fond/silver.jpg);")
        self.display=parcours.CardButton(flashcard.FlashCards(), self.gameArea, self.gameArea.frameSize().width()/5)
        self.layout.addWidget(self.display, 0, 0, 1, 1)
        self.editWidget=QWidget()
        self.editWidget.setFixedSize(self.display.frameSize())
        self.lineEdit=QLineEdit(self.editWidget)
        self.editWidgetLayout=QVBoxLayout(self.editWidget)
        self.editWidgetLayout.addWidget(self.lineEdit)
        #self.lineEdit.resize(self.gameArea.frameSize().width()/5, self.lineEdit.frameSize().height())
        self.layout.addWidget(QWidget(), 1, 0, 1, 1)
        self.layout.addWidget(self.editWidget, 2, 0, 1, 1)
        self.confirmShortcut=QShortcut(QtGui.QKeySequence('Return'), self.lineEdit, self.checkAnswer)

        #l'echelle : un degrade bleu -rouge
        self.degradeWidget=QLabel(self.gameArea)
        self.degradeWidget=self.degradeWidget
        self.degradeWidget.resize(self.gameArea.frameSize().width()*0.5, 35)
        self.pixmap=QtGui.QPixmap()
        path="view/icons/gradient.jpg"
        self.pixmap.load(path)
        self.pixmap=self.pixmap.scaled(self.degradeWidget.frameSize().width(), self.degradeWidget.frameSize().height()-30, QtCore.Qt.KeepAspectRatio)
        self.degradeWidget.setPixmap(self.pixmap)
        self.degradeWidget.setScaledContents(True)
        #on met une fenetre vide pour reserver de la place
        self.emptyWidget=QWidget(self.gameArea)
        self.emptyWidget.setVisible(False)
        self.emptyWidget.setFixedSize(20, self.gameArea.frameSize().height()*0.4)
        self.layout.addWidget(self.emptyWidget, 3, 0, 60, 1)
        #positionnement du degrade
        self.degradeWidget.move(self.gameArea.frameSize().width()*0.5-self.degradeWidget.frameSize().width()*0.5, self.gameArea.frameSize().height()*0.65)
        
        #un pointeur en-dessous du degrade
        self.pointeurWidget=QLabel(self.gameArea)
        self.pointeurWidget=self.pointeurWidget
        self.pointeurWidget.resize(45, 56)
        self.pixmap=QtGui.QPixmap()
        path="view/icons/fleche.png"
        self.pixmap.load(path)
        self.pointeurWidget.setPixmap(self.pixmap)
        #position initiale du pointeur
        self.leftMostPos=self.gameArea.frameSize().width()*0.5-self.pointeurWidget.frameSize().width()*0.5-self.degradeWidget.frameSize().width()*0.5
        self.rightMostPos=self.gameArea.frameSize().width()*0.5-self.pointeurWidget.frameSize().width()*0.5+self.degradeWidget.frameSize().width()*0.5  
        self.currentPointerPosition=self.leftMostPos
        self.currentPointerSpeed=0
        self.currentPointerTarget=self.currentPointerPosition
        self.pointeurWidget.move(self.currentPointerPosition, self.gameArea.frameSize().height()*0.76)
        
        #on reutilise le timer pour le mouvement fluide du pointeur
        self.timer.timeout.connect(self.movePointer)
        
        self.lineEdit.textEdited.connect(self.definePointerTarget)        
        
        self.resetSignal.connect(self.reset)
        self.newSignal.connect(self.new)
        self.chooseCards()
        self.initGame()
        self.show()
    def definePointerTarget(self):
        difference=rechercheFonct.DistanceDeDamerauLevenshtein(self.currentCard.trad, self.lineEdit.displayText())
        percentCorrespond=difference/len(self.currentCard.trad)
        self.currentPointerTarget=self.leftMostPos+max(len(self.currentCard.trad)-difference, 0)*self.degradeWidget.frameSize().width()/len(self.currentCard.trad)
    def movePointer(self):
        self.currentPointerSpeed=0.01*(self.currentPointerTarget-self.currentPointerPosition)
        self.currentPointerPosition+=self.currentPointerSpeed
        self.pointeurWidget.move(self.currentPointerPosition, self.gameArea.frameSize().height()*0.76)
    def checkAnswer(self):
        if (database.match(self.currentCard.word, self.lineEdit.displayText(), self.currentCard.tablename)):
            self.onSuccess()
        else:
            self.onFailure()
    #initialization for each word
    def initDisplay(self):
        self.display.setText(self.currentCard.word)
        self.lineEdit.setText(self.currentCard.trad[0:self.nbCharsDisplayed])
        #push the pointer to the leftmost position
        self.currentPointerPosition=self.leftMostPos
        self.currentPointerSpeed=0
        self.currentPointerTarget=self.currentPointerPosition
        self.pointeurWidget.move(self.currentPointerPosition, self.gameArea.frameSize().height()*0.76)
        self.lineEdit.setFocus(True)
    def onFailure(self):
        self.incrementErrorCount()
        self.nbCharsDisplayed+=1
        self.initDisplay()
    def onSuccess(self):
        self.incrementSuccessCount()
        if self.nbSucces>=self.nbSuccessRequired:
            return
        self.nbCharsDisplayed=0
        self.currentCardIndex+=1
        self.currentCard=self.cartesJouees[self.currentCardIndex]
        self.initDisplay()

    def timeIsOut(self):
        super().timeIsOut()
        self.lineEdit.setEnabled(False)
    def gameWon(self):
        super().gameWon()
        self.lineEdit.setEnabled(False)
    def initGame(self):
        super().initGame()
        self.nbCharsDisplayed=0
        self.currentCardIndex=0
        self.currentCard=self.cartesJouees[0]
        self.initDisplay()
    def clean(self):
        super().clean()
        self.lineEdit.setEnabled(True)
    def reset(self):
        self.clean()
        self.initGame()
    def new(self):
        self.chooseCards()
        self.reset()