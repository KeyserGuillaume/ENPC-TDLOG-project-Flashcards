from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QScrollArea, QScrollBar
import sys
from model import database

from view import editCardsInterf, rechercheInterf, viewCard, settingsInterf
from view.games import dragAndDrop, vraiOuFaux, hotCold, memory, pointToCard

from view.icons import icons
# permet l'accès aux images des icones

from math import ceil

AllLangages = database.giveAllLanguages()

#_root = QtCore.QFileInfo(__file__).absolutePath()

class LangageButton(QPushButton):
    def __init__(self, langue, place):
        self.langue=langue
        super(LangageButton, self).__init__(langue, place)
        self.setMinimumSize(QtCore.QSize(101, 91))
        self.setMaximumSize(QtCore.QSize(101, 91))
        self.setStyleSheet("background-image: url(:/icons/dossier.png);\n" "font: 75 14pt \"Arial\";")
        self.CardInterf = None
        self.clicked.connect(self.openChosenLanguage)
    openLanguageSignal=QtCore.pyqtSignal(str)

    def openChosenLanguage(self):
        # ouverture de l interface de parcours de cartes
        self.openLanguageSignal.emit(self.langue)
        #self.w=QWidget()
        #self.w.resize(800, 430)
        #self.CardInterf = parcoursChosenCards(self.w, self.langue)
        #self.w.show()

class parcoursLanguesFolder(QWidget):
    def __init__(self, parentWindow):
        super(parcoursLanguesFolder, self).__init__(parentWindow)
        parentWindow.resize(685, 430)
        self.resize(parentWindow.frameSize())
        self.gridWidget = QWidget(self)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(0, 0, 0, 0)
        AllLanguages=database.giveAllLanguages()
        self.myfolders = []
        for i, langue in enumerate(AllLangages):
            self.myfolders.append(LangageButton(langue, self.gridWidget))
            # 4 dossiers par ligne
            row = i/4
            column = i%4
            self.folderGrid.addWidget(self.myfolders[i], row, column, 1, 1)

        for i, langue in enumerate(AllLangages):
            self.myfolders[i].openLanguageSignal.connect(self.openLanguageSignal.emit)
    openLanguageSignal=QtCore.pyqtSignal(str)
    

class CardButton(QPushButton):
    def __init__(self, card, place, width):
        self.lacarte=card
        super(CardButton, self).__init__(card.word, place)
        self.setMinimumSize(QtCore.QSize(width, 0.66*width))
        self.setMaximumSize(QtCore.QSize(width, 0.66*width))
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);\n" "font: 75  \"Arial\";")
        self.clicked.connect(self.openChosenCard)
    openCardSignal=QtCore.pyqtSignal(str, str)

    def openChosenCard(self):
        self.openCardSignal.emit(self.lacarte.tablename, self.lacarte.word)

class CardButtonInRecherche(QPushButton):
    def __init__(self, card, rank, cardslist, place, width):
        self.allcards=cardslist
        self.lacarte=card
        self.lerang=rank
        super(CardButtonInRecherche, self).__init__(card.word, place)
        self.setMinimumSize(QtCore.QSize(width, 0.66*width))
        self.setMaximumSize(QtCore.QSize(width, 0.66*width))
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);\n" "font: 75  \"Arial\";")
        self.CardInterf = None
    openCardSignal=QtCore.pyqtSignal(list, int)

    def openGivenCard(self):
        self.openCardSignal.emit(self.allcards, self.lerang)


class CardsOverview(QScrollArea):
    """
    A compact view of cards. Cards may be found quickly in here.
    The givenCards argument may be "anglais" or another language, standing for
    all the cards of that language.
    """
    def __init__(self, parentWindow, givenCards):
        self.parentWindow = parentWindow
        self.cardslist=givenCards
        self.nextDisplay="abort"
    def stealTheLimelight(self):
        super(CardsOverview, self).__init__(self.parentWindow)
        languages = database.giveAllLanguages()
        if self.cardslist in languages:
            self.cardslist = database.getAllCards(self.cardslist)
        else:
            self.cardslist=database.updateCards(self.cardslist)
        ### il faudrait rajouter une barre de scrolling
        # et la possibilite de déplacement vertical
        self.setWindowTitle("Your Card selection")
        self.resize(self.parentWindow.frameSize())
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        #self.setWidgetResizable(True)
        self.gridWidget = QWidget(self)
        self.n=ceil(len(self.cardslist)/5)
        self.gridWidget.setGeometry(QtCore.QRect(0, 0, self.frameSize().width()-20, ((self.n+1)/36+self.n*0.11)*self.frameSize().width()))
        self.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.setWidget(self.gridWidget)
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(20, 20, 20, 20)
        self.cardButtons = []
        for i, carte in enumerate(self.cardslist):
            self.cardButtons.append(CardButton(carte, self.gridWidget, self.width()/6))
            # 5 cartes par ligne
            row = i/5
            column = i%5
            self.folderGrid.addWidget(self.cardButtons[i], row, column, 1, 1)

        for i in range(len(self.cardslist)):
            self.cardButtons[i].openCardSignal.connect(self.openCardLauncher)
        
        self.show()
    redirect=QtCore.pyqtSignal()
    def openCardLauncher(self, language, word):
        self.nextDisplay = viewCard.viewWindow(self.parentWindow, self.cardslist, word)
        self.redirect.emit()
    def toTheShadows(self):
        self.close()

class parcoursIconsGame(QWidget):
    def __init__(self, width, height, language):
        super(parcoursIconsGame, self).__init__()
        self.language=language
        self.setWindowTitle("Our Game selection")
        #self.resize(663, 406)
        self.resize(width, height)
        self.gridWidget = QWidget(self)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, self.frameSize().width()-22, self.frameSize().height()-45))
        self.gameGrid = QGridLayout(self.gridWidget)
        self.gameGrid.setContentsMargins(0, 0, 0, 0)
        # drag and drop game
        self.DDButton = QPushButton(u" ", self.gridWidget)
        self.DDButton.setMinimumSize(QtCore.QSize(101, 101))
        self.DDButton.setMaximumSize(QtCore.QSize(101, 101))
        self.DDButton.setStyleSheet("background-image: url(:/icons/dragdrop.png);")
        self.gameGrid.addWidget(self.DDButton, 0, 0, 1, 1)
        # memory game
        self.MemoryButton = QPushButton(u" ", self.gridWidget)
        self.MemoryButton.setMinimumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setMaximumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setStyleSheet("background-image: url(:/icons/memory.png);")
        self.gameGrid.addWidget(self.MemoryButton, 0, 1, 1, 1)
        # hot or cold game
        self.HCButton = QPushButton(u" ", self.gridWidget)
        self.HCButton.setMinimumSize(QtCore.QSize(101, 101))
        self.HCButton.setMaximumSize(QtCore.QSize(101, 101))
        self.HCButton.setStyleSheet("background-image: url(:/icons/hotcold.png);")
        self.gameGrid.addWidget(self.HCButton, 0, 2, 1, 1)
        # point the answer game
        self.pointButton = QPushButton(u" ", self.gridWidget)
        self.pointButton.setMinimumSize(QtCore.QSize(131, 101))
        self.pointButton.setMaximumSize(QtCore.QSize(131, 101))
        self.pointButton.setStyleSheet("background-image: url(:/icons/pointTo.png);")
        self.gameGrid.addWidget(self.pointButton, 0, 3, 1, 1)
        self.pointButton.setEnabled(False)
        # the right wrong game
        self.RWButton = QPushButton(u" ", self.gridWidget)
        self.RWButton.setMinimumSize(QtCore.QSize(101, 101))
        self.RWButton.setMaximumSize(QtCore.QSize(101, 101))
        self.RWButton.setStyleSheet("background-image: url(:/icons/rightWrong.png);")
        self.gameGrid.addWidget(self.RWButton, 0, 4, 1, 1)
        self.RWButton.setEnabled(False)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.DDInterf = None
        self.DDButton.clicked.connect(self.dragAndDropSignal.emit)
        self.RWButton.clicked.connect(self.rightWrongSignal.emit)
        self.HCButton.clicked.connect(self.hotAndColdSignal.emit)
        self.MemoryButton.clicked.connect(self.memorySignal.emit)
        self.pointButton.clicked.connect(self.pointSignal.emit)

    dragAndDropSignal=QtCore.pyqtSignal()
    memorySignal=QtCore.pyqtSignal()
    hotAndColdSignal=QtCore.pyqtSignal()
    pointSignal=QtCore.pyqtSignal()
    rightWrongSignal=QtCore.pyqtSignal()

#def main():
#    args = sys.argv
#    a = QApplication(args)
#    w=QWidget()
#    #w.resize(800, 430)
#    w.resize(600, 350)
#    mf = parcoursChosenCards(w, 'anglais')
#    w.show()
#    a.exec_()
#    a.lastWindowClosed.connect(a.quit)
#
#if __name__ == "__main__":
#    main()
