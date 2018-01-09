# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel
import sys
import database
from random import randrange



from time import time, strftime,localtime


class GameWindow (QWidget):
    def __init__(self, parentWindow, nbSuccessRequired):
        super(QWidget, self).__init__(parentWindow)
        self.nbSuccessRequired=nbSuccessRequired
        self.initGame()
    resetSignal=QtCore.pyqtSignal()
    timeIsOut=QtCore.pyqtSignal()
    gameWon=QtCore.pyqtSignal()
    def initGame(self):
        self.nberreurs=0
        self.nbSucces=0
        self.t0=time()
        self.timeGiven=60
        ## la fenetre
        self.setObjectName("Jeu de reliage")
        self.setWindowTitle("Drag and Drop")
        #self.setFixedSize(853, 554)
        self.resize(self.parent().frameSize())
        ## le jeu comme defini ci dessus
        self.gameArea=QWidget(self)
        self.gameArea.resize(833, 423)
        #self.theGame=DragDropGame(self, self.myCards)
        ## la barre de boutons/compteurs du bas
        self.BottomWidget = QWidget(self)
        self.BottomWidget.setGeometry(QtCore.QRect(10, 440, 731, 61))
        self.BottomWidget.setObjectName("BottomWidget")
        self.GameBox = QHBoxLayout(self.BottomWidget)
        self.GameBox.setContentsMargins(0, 0, 0, 0)
        self.GameBox.setObjectName("GameBox")
        # les boutons de gestion de partie
        self.newButton = QPushButton(u"New Round",self.BottomWidget)
        self.newButton.setObjectName("newButton")
        self.GameBox.addWidget(self.newButton)
        self.saveButton = QPushButton(u"Save Round", self.BottomWidget)
        self.saveButton.setObjectName("saveButton")
        self.GameBox.addWidget(self.saveButton)
        self.resetButton = QPushButton(u"Reset",self.BottomWidget)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.resetSignal.emit)
        self.GameBox.addWidget(self.resetButton)
        # compteur chrono
        self.chrono = QLCDNumber(self.BottomWidget)
        self.chrono.setDigitCount(2)
        self.chrono.setObjectName("chrono")
        self.GameBox.addWidget(self.chrono)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(10)
        # bouton pour afficher ses erreurs
        self.mistakesButton = QPushButton(u"See mistakes",self.BottomWidget)
        self.mistakesButton.setObjectName("mistakesButton")
        self.GameBox.addWidget(self.mistakesButton)
        # compteur d'erreurs
        self.failure = QLCDNumber(self.BottomWidget)
        self.failure.setStyleSheet("color: rgb(252, 0, 6);\n" "border-color: rgb(0, 0, 0);\n" "")
        self.failure.setDigitCount(5)
        self.failure.setObjectName("failure")
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.Mistake)
        self.timer2.start(10)
        self.GameBox.addWidget(self.failure)
        
    def incrementSuccessCount(self):
        self.nbSucces+=1;
        if (self.nbSucces==self.nbSuccessRequired):
            self.gameWon.emit()
        
    def incrementErrorCount(self):
        self.nberreurs+=1
    def Time(self):
        if (self.nbSucces==self.nbSuccessRequired):
            return
        #currenttime = time()-t0
        # affiche l'heure
        # regarder doc de time pour changer en un chrono descendant
        timeLeft=self.timeGiven-(time()-self.t0)//1
        if (timeLeft<0) :
            self.timeIsOut.emit()
            return
        self.chrono.display(timeLeft)
        #self.chrono.display(strftime("%H" + ":" + "%M" + ":" + "%S", localtime()))

#    def reset(self):
#        self.theGame.close()
#        self.BottomWidget.close()
#        self.initGame()
#        self.resetSignal.emit()
#        self.theGame.show()
#        self.BottomWidget.show()
#        self.theGame.victoryWidget.setVisible(False)
    def Mistake(self):
        self.failure.display(self.nberreurs)



if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)
    args = sys.argv
    b = QApplication(args)
    mf = GameWindow(CartesEnJeu)
    mf.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
