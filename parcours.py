from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QScrollArea, QScrollBar
import sys
import database

import dragAndDrop
import viewCard

from icons import icons
# permet l'accès aux images des icones

from math import ceil

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
    def __init__(self, card, rank, cardslist, place):
        self.allcards=cardslist
        self.lacarte=card
        self.lerang=rank
        super(CardButton, self).__init__(card.word, place)
        self.setMinimumSize(QtCore.QSize(151, 111))
        self.setMaximumSize(QtCore.QSize(151, 111))
        #self.setStyleSheet("background-image: url(:/icons/fcard.png);\n" "background-color: rgba(255, 255, 255, 0);\n" "font: 75 18pt \"Arial\";")
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);\n" "font: 75 18pt \"Arial\";")
        self.setObjectName(card.word)
        self.CardInterf = None

    def openChosenCard(self):
        # ouverture de l interface de parcours de cartes
        #self.CardInterf = viewCard.ViewDialog(self.lacarte.name-1, self.allcards)
        # ne marche plus car certains noms ne sont plus attribués dans anglais (2,4,5,7,8,12,13)
        # donc plus de lien direct entre rang et nom
        self.w=QWidget()
        self.CardInterf = viewCard.viewDialog(self.w, self.lerang, self.allcards)
        self.w.show()

class parcoursChosenCards(object):
    def __init__(self, langue):
        self.cardslist=database.getAllCards(langue)
        ### il faudrait rajouter une barre de scrolling
        # et la possibilité de déplacement vertical
        self.Dialog = QScrollArea()  #QWidget()
        self.Dialog.setObjectName("SelectCard")
        self.Dialog.setWindowTitle("Your Card selection")
        self.Dialog.setGeometry(QtCore.QRect(0, 0, 800, 430))
        self.Dialog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.Dialog.setWidgetResizable(True)
        self.gridWidget = QWidget(self.Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(0, 0, 760, 131*ceil(len(self.cardslist)/5)))
        self.gridWidget.setObjectName("grille de placement")
        self.gridWidget.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.Dialog.setWidget(self.gridWidget)
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(20, 20, 20, 20)
        self.folderGrid.setObjectName("folderGrid")
        self.mycards = self.cardslist.copy()
        #print([x.word for x in self.cardslist])
        #print([x.name for x in self.cardslist])
        #### certains noms ne sont pas attribués dans anglais (2,4,5,7,8,12,13)
        for i, carte in enumerate(self.cardslist):
            self.mycards[i] = CardButton(carte, i, self.cardslist, self.gridWidget)
            # 5 cartes par ligne
            row = i/5
            column = i%5
            self.folderGrid.addWidget(self.mycards[i], row, column, 1, 1)

        for i, carte in enumerate(self.cardslist):
            self.mycards[i].clicked.connect(self.mycards[i].openChosenCard)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()

class parcoursIconsGame(QWidget):
    def __init__(self, width, height, language):
        super(parcoursIconsGame, self).__init__()
        self.language=language
        self.setObjectName("SelectGame")
        self.setWindowTitle("Our Game selection")
        #self.resize(663, 406)
        self.resize(width, height)
        self.gridWidget = QWidget(self)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, self.frameSize().width()-22, self.frameSize().height()-45))
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
        self.DDButton.clicked.connect(self.dragAndDropSignal.emit)
    dragAndDropSignal=QtCore.pyqtSignal()
    memorySignal=QtCore.pyqtSignal()
    hotAndColdSignal=QtCore.pyqtSignal()
    pointSignal=QtCore.pyqtSignal()
    rightWrongSignal=QtCore.pyqtSignal()
    def show(self):
        # ouverture de la fenetre
        self.show()
"""
    def openDD(self):
        # ouverture de l'interface de jeu
    #a remplacer qd on aura vire les dimensions absolues
        self.w = QWidget()
        self.w.resize(853, 554)
        self.DDInterf = dragAndDrop.dragDropGame(self.w, database.getCardsToLearn(self.language,0,10))
        self.w.show()
        self.DDInterf.show()
"""
def main():
    args = sys.argv
    a = QApplication(args)
    mf = parcoursChosenCards('anglais')
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
