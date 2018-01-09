from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QPushButton
import sys
import database

from math import ceil

#import dragAndDrop

from icons import icons

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
        # changement de coté de la carte
        if self.laface == 0:
            self.setStyleSheet("background-image: url(:/fond/yellow.jpg);\n" "font: 87 13pt \"Arial Black\";")
            if self.lanature == 0:
                self.setText(self.lacarte.word)
            else:
                self.setText(self.lacarte.trad)
            self.laface = 1
        elif self.laface == 1:
            self.setStyleSheet("background-image: url(:/fond/green.jpg);\n" "font: 87 13pt \"Arial Black\";")
            self.setText(" ")
            self.laface = 0
        ## gere le cas de deja en paire : self.setStyleSheet("background-image: url(:/fond/silver.jpg);\n" "font: 87 13pt \"Arial Black\";")

### le widget de jeu (carte qur un plateau qui se retournent
class MemoryGame(QScrollArea):
    def __init__(self,bigWindow, CardsPlayed, width, height):
        self.cardslist = CardsPlayed
        print([x.word for x in self.cardslist])
        ## la fenetre
        super(MemoryGame, self).__init__(bigWindow)
        self.setObjectName("Jeu de memoire")
        bigWindow.setWindowTitle("Memory")
        self.setGeometry(QtCore.QRect(0, 0, width, height))
        self.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plateau = QWidget(self)
        self.plateau.setGeometry(QtCore.QRect(20, 20, 670, 120*ceil(2*len(self.cardslist)/5)))
        print(100*ceil(2*len(self.cardslist)/5))
        self.plateau.setObjectName("plateau de jeu")
        self.plateau.setStyleSheet("background-image: url(:/fond/wood.jpg);")
        self.gridLayout = QGridLayout(self.plateau)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.mycards = list(range(2 * len(self.cardslist) ))
        for i, carte in enumerate(self.cardslist):
            self.mycards[2*i] = PlayingCard(carte, 0, self.plateau)
            self.mycards[2*i+1] = PlayingCard(carte, 1, self.plateau)

        for i in range(len(self.mycards)):
            # 5 cartes par ligne
            row = i / 5
            column = i % 5
            self.gridLayout.addWidget(self.mycards[i], row, column, 1, 1)

        self.setWidget(self.plateau)

        for i in range(len(self.mycards)):
            self.mycards[i].clicked.connect(self.mycards[i].flip)


if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)
    args = sys.argv
    b = QApplication(args)
    #mf = GameWindow(CartesEnJeu)
    window = QWidget()
    mf = MemoryGame(window,CartesEnJeu, 700, 440)
    window.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
