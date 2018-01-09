from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QScrollArea, QScrollBar
import sys
import database

import dragAndDrop
import viewCard

from icons import icons
# permet l'accès aux images des icones

AllLangages = database.giveAllLanguages()

_root = QtCore.QFileInfo(__file__).absolutePath()

class LangageButton(QPushButton):
    def __init__(self, langue, place):
        self.langue=langue
        super(LangageButton, self).__init__(langue, place)
        self.setMinimumSize(QtCore.QSize(101, 91))
        self.setMaximumSize(QtCore.QSize(101, 91))
        self.setStyleSheet("background-image: url(:/icons/dossier.png);\n" "font: 75 14pt \"Arial\";")
        self.setObjectName(langue)
        self.CardInterf = None

    def openChosenCard(self):
        # ouverture de l interface de parcours de cartes
        self.CardInterf = parcoursChosenCards(self.langue)
        self.CardInterf.show()

class parcoursLanguesFolder(object):
    def __init__(self, Dialog):
        Dialog.resize(685, 430)
        self.gridWidget = QWidget(Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setObjectName("grille de placement")
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(0, 0, 0, 0)
        self.folderGrid.setObjectName("folderGrid")
        self.myfolders = AllLangages.copy()
        for i, langue in enumerate(AllLangages):
            self.myfolders[i] = LangageButton(langue, self.gridWidget)
            # 4 dossiers par ligne
            row = i/4
            column = i%4
            self.folderGrid.addWidget(self.myfolders[i], row, column, 1, 1)

        for i, langue in enumerate(AllLangages):
            self.myfolders[i].clicked.connect(self.myfolders[i].openChosenCard)

class CardButton(QPushButton):
    def __init__(self, card, cardslist, place):
        self.allcards=cardslist
        self.lacarte=card
        super(CardButton, self).__init__(card.word, place)
        self.setMinimumSize(QtCore.QSize(151, 111))
        self.setMaximumSize(QtCore.QSize(151, 111))
        #self.setStyleSheet("background-image: url(:/icons/fcard.png);\n" "font: 75 18pt \"Arial\";")
        self.setObjectName(card.word)
        self.CardInterf = None

    def openChosenCard(self):
        # ouverture de l interface de parcours de cartes
        self.CardInterf = viewCard.ViewDialog(self.lacarte.name-1, self.allcards)
        self.CardInterf.show()

class parcoursChosenCards(object):
    def __init__(self, langue):
        self.cardslist=database.getAllCards(langue)
        ### il faudrait rajouter une barre de scrolling
        # et la possibilité de déplacement vertical
        self.Dialog = QScrollArea()  #QWidget()
        self.Dialog.setObjectName("SelectCard")
        self.Dialog.setWindowTitle("Your Card selection")
        self.Dialog.setGeometry(QtCore.QRect(0, 0, 780, 430))
        self.Dialog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.Dialog.setWidgetResizable(True)
        self.gridWidget = QWidget(self.Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 760, 111*(len(self.cardslist)/5+1)))
        self.gridWidget.setObjectName("grille de placement")
        self.gridWidget.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.Dialog.setWidget(self.gridWidget)
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(0, 0, 0, 0)
        self.folderGrid.setObjectName("folderGrid")
        self.scrollbar = QScrollBar()
        self.mycards = self.cardslist.copy()
        for i, carte in enumerate(self.cardslist):
            self.mycards[i] = CardButton(carte, self.cardslist, self.gridWidget)
            # 5 dossiers par ligne
            row = i/5
            column = i%5
            self.folderGrid.addWidget(self.mycards[i], row, column, 1, 1)

        for i, carte in enumerate(self.cardslist):
            self.mycards[i].clicked.connect(self.mycards[i].openChosenCard)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()

class parcoursIconsGame(object):
    def __init__(self):
        self.Dialog = QWidget()
        self.Dialog.setObjectName("SelectGame")
        self.Dialog.setWindowTitle("Our Game selection")
        self.Dialog.resize(663, 406)
        self.gridWidget = QWidget(self.Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setObjectName("gridWidget")
        self.gameGrid = QGridLayout(self.gridWidget)
        self.gameGrid.setContentsMargins(0, 0, 0, 0)
        self.gameGrid.setObjectName("gameGrid")
        # drag and drop game
        self.DDButton = QPushButton(u" ", self.gridWidget)
        self.DDButton.setMinimumSize(QtCore.QSize(101, 101))
        self.DDButton.setMaximumSize(QtCore.QSize(101, 101))
        self.DDButton.setStyleSheet("background-image: url(:/icons/dragdrop.png);")
        self.DDButton.setObjectName("DDButton")
        self.gameGrid.addWidget(self.DDButton, 0, 0, 1, 1)
        # memory game
        self.MemoryButton = QPushButton(u" ", self.gridWidget)
        self.MemoryButton.setMinimumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setMaximumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setStyleSheet("background-image: url(:/icons/memory.png);")
        self.MemoryButton.setObjectName("MemoryButton")
        self.gameGrid.addWidget(self.MemoryButton, 0, 1, 1, 1)
        # hot or cold game
        self.HCButton = QPushButton(u" ", self.gridWidget)
        self.HCButton.setMinimumSize(QtCore.QSize(101, 101))
        self.HCButton.setMaximumSize(QtCore.QSize(101, 101))
        self.HCButton.setStyleSheet("background-image: url(:/icons/hotcold.png);")
        self.HCButton.setObjectName("HCButton")
        self.gameGrid.addWidget(self.HCButton, 0, 2, 1, 1)
        # point the answer game
        self.pointButton = QPushButton(u" ", self.gridWidget)
        self.pointButton.setMinimumSize(QtCore.QSize(131, 101))
        self.pointButton.setMaximumSize(QtCore.QSize(131, 101))
        self.pointButton.setStyleSheet("background-image: url(:/icons/pointTo.png);")
        self.pointButton.setObjectName("pointButton")
        self.gameGrid.addWidget(self.pointButton, 0, 3, 1, 1)
        # the right wrong game
        self.RWButton = QPushButton(u" ", self.gridWidget)
        self.RWButton.setMinimumSize(QtCore.QSize(101, 101))
        self.RWButton.setMaximumSize(QtCore.QSize(101, 101))
        self.RWButton.setStyleSheet("background-image: url(:/icons/rightWrong.png);")
        self.RWButton.setObjectName("RWButton")
        self.gameGrid.addWidget(self.RWButton, 0, 4, 1, 1)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.DDInterf = None
        self.DDButton.clicked.connect(self.openDD)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()

    def openDD(self):
        # ouverture de l'interface de jeu
        self.DDInterf = dragAndDrop.GameWindow(database.getCardsToLearn('anglais',0,10))
        self.DDInterf.show()

def main():
    args = sys.argv
    a = QApplication(args)
    mf = parcoursChosenCards('anglais')
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
