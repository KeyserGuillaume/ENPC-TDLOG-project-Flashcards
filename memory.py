from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QPushButton, QLabel
import sys
import database

from math import ceil
from random import shuffle

import gameWindow

from icons import icons

yellowcards=[]

def matchingCards():
    #si 2 carte retournees
    if len(yellowcards)==2:
        # nature differente (un mot et une trad)
        if yellowcards[0].lanature != yellowcards[1].lanature :
            # cartes correspondantes
            if yellowcards[0].lacarte.word == yellowcards[1].lacarte.word :
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class PlayingCard(QPushButton):
    def __init__(self, card, type, place):
        super(PlayingCard, self).__init__(place)
        self.lacarte = card
        self.lanature = type # carte de mot (0) ou de trad (1)
        self.laface = 0 # 0 si coté caché, 1 si coté écrit, 2 si deja en paire
        self.setMinimumSize(QtCore.QSize(100, 80))
        self.setMaximumSize(QtCore.QSize(100, 80))
        self.setStyleSheet("background-image: url(:/fond/green.jpg);\n" "font: 87 13pt \"Arial Black\";")

    def flip(self):
        global yellowcards
        current = len(yellowcards)
        # changement de coté de la carte
        if self.laface == 0 and current < 2:
            self.setStyleSheet("background-image: url(:/fond/yellow.jpg);\n" "font: 87 13pt \"Arial Black\";")
            current += 1
            if self.lanature == 0:
                self.setText(self.lacarte.word)
            else:
                self.setText(self.lacarte.trad)
            self.laface = 1
            yellowcards.append(self)
        elif self.laface == 1 and current>0:
            self.setStyleSheet("background-image: url(:/fond/green.jpg);\n" "font: 87 13pt \"Arial Black\";")
            self.setText(" ")
            self.laface = 0
            current-=1
            yellowcards.remove(self)
        ## gere le cas de deja en paire :
        if matchingCards():
            for matchedcard in yellowcards :
                matchedcard.setStyleSheet("background-image: url(:/fond/silver.jpg);\n" "font: 87 13pt \"Arial Black\";")
                matchedcard.laface = 2
                matchedcard.setEnabled(False)
            yellowcards = []

### le widget de jeu (carte sur un plateau qui se retournent)
class MemoryGame(QScrollArea):
    def __init__(self,bigWindow, CardsPlayed, width, height):
        ## les flashcards en jeu
        self.cardslist = CardsPlayed
        ## la fenetre ( widget avec scroll bar)
        super(MemoryGame, self).__init__(bigWindow)
        self.setObjectName("Jeu de memoire")
        bigWindow.setWindowTitle("Memory")
        self.setGeometry(QtCore.QRect(0, 0, width, height))
        self.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plateau = QWidget(self)
        self.plateau.setGeometry(QtCore.QRect(20, 20, 670, 120*ceil(2*len(self.cardslist)/5)))
        self.plateau.setObjectName("plateau de jeu")
        self.plateau.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.gridLayout = QGridLayout(self.plateau)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        # creation des cartes de jeu a raison de 2 par flashcard en jeu
        self.mycards = list(range(2 * len(self.cardslist) ))
        for i, carte in enumerate(self.cardslist):
            self.mycards[2*i] = PlayingCard(carte, 0, self.plateau)
            self.mycards[2*i+1] = PlayingCard(carte, 1, self.plateau)

        # on mélange les cartes
        shuffle(self.mycards)
        # affichage des cartes
        for i in range(len(self.mycards)):
            # 5 cartes par ligne
            row = i / 5
            column = i % 5
            self.gridLayout.addWidget(self.mycards[i], row, column, 1, 1)
        self.setWidget(self.plateau)

        # nombre et donnes des cartes retournees (au max 2 donc 0 ou 1 ou 2)
        global yellowcards
        yellowcards = []

        # le message de victoire
        self.victoryWidget = QWidget(self)
        self.victoryWidget.resize(300, 200)
        qr = self.victoryWidget.frameGeometry()
        qr.moveCenter(self.rect().center())
        self.victoryWidget.move(qr.topLeft())
        self.label = QLabel(self.victoryWidget)
        path = "icons/victory.png"
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(path)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.victoryWidget.setVisible(False)

        # le message de defaite
        self.defeatWidget = QWidget(self)
        self.defeatWidget.resize(300, 200)
        qr = self.defeatWidget.frameGeometry()
        qr.moveCenter(self.rect().center())
        self.defeatWidget.move(qr.topLeft())
        self.label = QLabel(self.defeatWidget)
        path = "icons/gameOver.png"
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(path)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.defeatWidget.setVisible(False)

        # connection slots et signaux
        for i in range(len(self.mycards)):
            self.mycards[i].clicked.connect(self.mycards[i].flip)
            self.mycards[i].clicked.connect(self.checkAnswer)

    running = QtCore.pyqtSignal()
    success = QtCore.pyqtSignal()
    def checkAnswer(self):
        allassociated = True
        for i in range(len(self.mycards)):
            allassociated = allassociated and not(self.mycards[i].isEnabled())
        if allassociated :
            self.success.emit()
        else:
            self.running.emit()
    def onVictory(self):
        self.victoryWidget.show()
    def onDefeat(self):
        self.defeatWidget.show()


class MemoryGameWindow(QWidget):
    def __init__(self, givenWindow, cardsPlayed):
        super(MemoryGameWindow, self).__init__(givenWindow)
        self.resize(givenWindow.frameSize())
        self.cardslist = cardsPlayed
        self.nbCharsDisplayed = 0
        self.window = gameWindow.GameWindow(self, len(self.cardslist))
        self.game = MemoryGame(self.window.gameArea, self.cardslist, self.window.gameArea.width(), self.window.gameArea.height())
        self.window.show()

        self.window.resetSignal.connect(self.reset)
        self.window.leaveSignal.connect(self.endOfGame)
        self.game.success.connect(self.game.onVictory)
        self.window.timeIsOut.connect(self.game.onDefeat)

    leave = QtCore.pyqtSignal()

    def reset(self):
        self.game.close()
        self.window.timeIsOut.disconnect()
        self.window.close()
        self.init()

    def endOfGame(self):
        self.leave.emit()
        self.close()

if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)[0:10]
    args = sys.argv
    b = QApplication(args)
    #mf = GameWindow(CartesEnJeu)
    window = QWidget()
    #mf = MemoryGame(window,CartesEnJeu, 700, 440)
    mf = MemoryGameWindow(window, CartesEnJeu)
    window.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
