from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout, QLabel, QShortcut
import sys

from model import database, soundAPI
from view import editCardsInterf

from view.icons import icons
# permet l'acces aux images des icones

class viewWindow(QWidget):
    def __init__(self, parentWindow, givenCards, word=None, nextWord=None, view=0):
        #here, givenCards may be "anglais" ou une autre langue, pour signifier toutes les cartes de cette langue
        #basically, nextWord is the word to begin with if word was deleted
        self.originalGivenCards = givenCards
        self.word = word
        self.nextWord = nextWord
        self.parentWindow = parentWindow
        self.currentview = view
        self.previousview = 0
    def stealTheLimelight(self):
        super(QWidget, self).__init__(self.parentWindow)
        self.resize(self.parentWindow.frameSize())
        # si givenCards est une langue, on les recupere toutes de cette langue
        languages = database.giveAllLanguages()
        if self.originalGivenCards in languages:
            self.givenCards = database.getAllCards(self.originalGivenCards)
        else:
            self.givenCards = database.updateCards(self.originalGivenCards)
        # le nombre de cartes
        self.nbCard=len(self.givenCards)
        # le widget de vue
        self.background = QWidget(self)
        self.background.resize(self.frameSize())
        self.background.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        #self.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.viewbar = QHBoxLayout(self.background)
        self.viewbar.setContentsMargins(0, 0, 0, 0)
        # le bouton precedent
        self.previous = QPushButton(u" ", self.background)
        self.previous.setMinimumSize(QtCore.QSize(71, 71))
        self.previous.setMaximumSize(QtCore.QSize(71, 71))
        self.previous.setStyleSheet("background-image: url(:/icons/previous.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.viewbar.addWidget(self.previous)
        # find the word if any was asked for
        if self.word is not None:
            self.findWord(self.word)
        self.cardWindow = QWidget(self.background)
        self.cardWindow.setMinimumSize(QtCore.QSize(361, 251))
        self.cardWindow.setMaximumSize(QtCore.QSize(361, 251))
        self.currentCard = self.givenCards[self.cardnumber]
        #####################################THE CENTER###############################################################################
        self.cardWindow.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);")
        # le layout separant contenu et outils
        self.gridLayoutWidget = QWidget(self.cardWindow)
        self.gridLayoutWidget.resize(self.cardWindow.frameSize())
        self.viewNtools = QGridLayout(self.gridLayoutWidget)
        self.viewNtools.setContentsMargins(0, 0, 0, 0)
        # bouton edit
        self.editButton = QPushButton(u" ", self.gridLayoutWidget)
        self.editButton.setMinimumSize(QtCore.QSize(31, 32))
        self.editButton.setMaximumSize(QtCore.QSize(31, 32))
        self.editButton.setStyleSheet("background-image: url(:/icons/edit.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.viewNtools.addWidget(self.editButton, 2, 0, 1, 1)
        # bouton flip
        self.flipButton = QPushButton(u" ", self.gridLayoutWidget)
        self.flipButton.setMinimumSize(QtCore.QSize(41, 32))
        self.flipButton.setMaximumSize(QtCore.QSize(41, 32))
        self.flipButton.setStyleSheet("background-image: url(:/icons/flip.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.viewNtools.addWidget(self.flipButton, 2, 2, 1, 1)
        # bouton picture
        self.pictureButton = QPushButton(u" ", self.gridLayoutWidget)
        self.pictureButton.setMinimumSize(QtCore.QSize(41, 31))
        self.pictureButton.setMaximumSize(QtCore.QSize(41, 31))
        self.pictureButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "background-image: url(:/icons/picture.png);")
        self.viewNtools.addWidget(self.pictureButton, 0, 2, 1, 1)
        # bouton sound
        self.soundButton = QPushButton(u" ", self.gridLayoutWidget)
        self.soundButton.setMinimumSize(QtCore.QSize(31, 32))
        self.soundButton.setMaximumSize(QtCore.QSize(31, 32))
        self.soundButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "background-image: url(:/icons/speaker.png);")
        self.viewNtools.addWidget(self.soundButton, 0, 0, 1, 1)

        # les faces mot, info et image
        self.getFaces()

        # signaux et slots
        self.flipButton.clicked.connect(self.flipping)
        self.pictureButton.clicked.connect(self.flipPicture)
        self.modifInterf=None
        self.editButton.clicked.connect(self.cardModificationLauncher)
        self.soundButton.clicked.connect(self.playSound)
        #####################################END OF THE CENTER###############################################################################
        self.viewbar.addWidget(self.cardWindow)
        # le bouton suivant
        self.next = QtWidgets.QPushButton(u" ", self.background)
        self.next.setMinimumSize(QtCore.QSize(71, 71))
        self.next.setMaximumSize(QtCore.QSize(71, 71))
        self.next.setStyleSheet("background-image: url(:/icons/next.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.viewbar.addWidget(self.next)
        
        #shortcuts
        self.nextShortcut=QShortcut(QtGui.QKeySequence('Right'), self)
        self.prevShortcut=QShortcut(QtGui.QKeySequence('Left'), self)
        self.flipShortcut=QShortcut(QtGui.QKeySequence('Ctrl+f'), self)


        ## signaux et slots : ouverture de la fenetre de jeux
        self.next.clicked.connect(self.toNextCard)
        self.previous.clicked.connect(self.toPreviousCard)
        self.nextShortcut.activated.connect(self.toNextCard)
        self.prevShortcut.activated.connect(self.toPreviousCard)
        self.flipShortcut.activated.connect(self.flipping)
        
        self.show()
    redirect=QtCore.pyqtSignal()
    def findWord(self, word):
        self.cardnumber = 0
        while self.cardnumber < len(self.givenCards) and word!=self.givenCards[self.cardnumber].word:
            self.cardnumber+=1
        if self.cardnumber == len(self.givenCards):
            if self.nextWord is not None: # in case of deletion of previous word
                self.findWord(self.nextWord)
            else:
                print("viewWindow::stealTheLimelight: the word is not part of the given list")
        if self.cardnumber == len(self.givenCards):
            self.cardnumber = 0
    
    def getFaces(self):
        # la face Mot
        self.viewWidget0 = QWidget(self.cardWindow)
        self.viewWidget0.resize(self.cardWindow.frameSize())
        self.viewLayout0 = QVBoxLayout(self.viewWidget0)
        self.mot = QPushButton(self.currentCard.word, self.viewWidget0)
        self.mot.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 18pt \"Arial Black\";")
        self.viewLayout0.addWidget(self.mot)
        self.viewWidget0.setVisible(False)
        # la face Infos
        self.viewWidget1 = QWidget(self.cardWindow)
        self.viewWidget1.resize(self.cardWindow.frameSize())
        self.viewLayout1 = QVBoxLayout(self.viewWidget1)
        self.description = QPushButton(self.currentCard.shortStr(), self.viewWidget1)
        self.description.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 11pt \"Arial Black\";")
        self.viewLayout1.addWidget(self.description)
        self.viewWidget1.setVisible(False)
        # la face Image
        path = self.currentCard.image
        if path == '':
            path = 'images/image.jpg'
        self.viewWidget2 = QLabel(self)
        self.viewWidget2.setAlignment(QtCore.Qt.AlignCenter)
        self.viewWidget2.resize(self.cardWindow.frameSize().width()-100, self.cardWindow.frameSize().height()-60)
        self.pixmap = QtGui.QPixmap()
        
        self.pixmap.load(path)
        self.pixmap = self.pixmap.scaled(self.viewWidget2.frameSize().width(),
                                         self.viewWidget2.frameSize().height(),
                                         QtCore.Qt.KeepAspectRatio)
        self.viewWidget2.setPixmap(self.pixmap)
        #self.viewWidget2.setScaledContents(True)
        self.viewWidget2.setVisible(False)
        # affichage de la bonne face
        self.viewWidgets = [self.viewWidget0, self.viewWidget1, self.viewWidget2]
        self.viewNtools.addWidget(self.viewWidgets[self.currentview], 1, 1, 1, 1)
        self.viewWidgets[self.currentview].setVisible(True)
            
    def alternateViews(self):
        self.viewNtools.removeWidget(self.viewWidgets[self.previousview])
        self.viewNtools.addWidget(self.viewWidgets[self.currentview], 1, 1, 1, 1)
        self.viewWidgets[self.previousview].setVisible(False)
        self.viewWidgets[self.currentview].setVisible(True)

    def flipping(self):
        self.previousview = self.currentview
        if self.previousview==0:    #face mot -> face carte
            self.currentview = 1
        elif self.previousview==1 or self.previousview==2:    #face carte ou image -> face mot
            self.currentview = 0    
        self.alternateViews()
       
    def flipPicture(self):
        if self.currentview==2:
            (self.previousview, self.currentview)=(self.currentview, self.previousview)
        else:
            self.previousview = self.currentview
            self.currentview = 2
        self.alternateViews()
        
    def playSound(self):
        soundAPI.playSoundFromFile(self.currentCard.pronounciation)
    
    #what happens when we modify is we give a cardmodification object as next display,
    #but this object contains the correct display that must follow
    def cardModificationLauncher(self):
        if self.cardnumber==len(self.givenCards)-1:
            nextWord = self.givenCards[self.cardnumber-1].word
        else:
            nextWord = self.givenCards[self.cardnumber+1].word
        postModificationDisplay = viewWindow(self.parentWindow, self.originalGivenCards, self.currentCard.word, nextWord, self.currentview)
        self.nextDisplay = editCardsInterf.CardModification(self.parentWindow, self.currentCard, postModificationDisplay)
        self.redirect.emit()
    def toNextCard(self):
        if self.cardnumber < self.nbCard-1:
            self.cardnumber += 1
            #changement de carte (dans l'ordre des noms) vers +1
            self.currentCard = self.givenCards[self.cardnumber]
            self.previous.setEnabled(True)
            self.word = self.givenCards[self.cardnumber].word
        else:
            self.next.setEnabled(False)
        self.getFaces()
    def toPreviousCard(self):
        if self.cardnumber>0:
            self.cardnumber -= 1
            #changement de carte (dans l'ordre des noms) vers -1
            self.currentCard = self.givenCards[self.cardnumber]
            self.next.setEnabled(True)
            self.word=self.givenCards[self.cardnumber].word
        else:
            self.previous.setEnabled(False)
        self.getFaces()
    def toTheShadows(self):
        self.close()