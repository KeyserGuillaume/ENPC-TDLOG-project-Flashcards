from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout, QLabel, QShortcut
import sys

import database, createcardsInterf


## a lier au layout du cote de interfaccueil

from icons import icons
# permet l'accès aux images des icones


### pour l'instant un probleme inconnu limite a un seul flip visuel par carte -> Pb regle

class CardWidget(QWidget):
    def __init__(self, card, parentWindow, view=0):
        super(CardWidget, self).__init__(parentWindow)
        # sauvegarde des donnees de la carte pour le flip
        self.card=card
        # la face affichee
        ### petit probleme avec de l'affichage laminaire en changent de face (widgets, ...)
        self.currentview=view
        # les caracteristiques du widget de la carte
        self.setMinimumSize(parentWindow.frameSize())
        self.setMaximumSize(parentWindow.frameSize())
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);")
        self.setObjectName("Card")
        # le layout separant contenu et outils
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.resize(self.frameSize())
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.viewNtools = QGridLayout(self.gridLayoutWidget)
        self.viewNtools.setContentsMargins(0, 0, 0, 0)
        self.viewNtools.setObjectName("viewNtools")
        # bouton edit
        self.editButton = QPushButton(u" ", self.gridLayoutWidget)
        self.editButton.setMinimumSize(QtCore.QSize(31, 32))
        self.editButton.setMaximumSize(QtCore.QSize(31, 32))
        self.editButton.setStyleSheet("background-image: url(:/icons/edit.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.editButton.setObjectName("editButton")
        self.viewNtools.addWidget(self.editButton, 2, 0, 1, 1)
        # bouton flip
        self.flipButton = QPushButton(u" ", self.gridLayoutWidget)
        self.flipButton.setMinimumSize(QtCore.QSize(41, 32))
        self.flipButton.setMaximumSize(QtCore.QSize(41, 32))
        self.flipButton.setStyleSheet("background-image: url(:/icons/flip.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.flipButton.setObjectName("flipButton")
        self.viewNtools.addWidget(self.flipButton, 2, 2, 1, 1)
        # bouton picture
        self.pictureButton = QPushButton(u" ", self.gridLayoutWidget)
        self.pictureButton.setMinimumSize(QtCore.QSize(41, 31))
        self.pictureButton.setMaximumSize(QtCore.QSize(41, 31))
        self.pictureButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "background-image: url(:/icons/picture.png);")
        self.pictureButton.setObjectName("pictureButton")
        self.viewNtools.addWidget(self.pictureButton, 0, 2, 1, 1)
        # bouton sound
        self.soundButton = QPushButton(u" ", self.gridLayoutWidget)
        self.soundButton.setMinimumSize(QtCore.QSize(31, 32))
        self.soundButton.setMaximumSize(QtCore.QSize(31, 32))
        self.soundButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "background-image: url(:/icons/speaker.png);")
        self.soundButton.setObjectName("soundButton")
        self.viewNtools.addWidget(self.soundButton, 0, 0, 1, 1)
        # la face Mot
        self.viewWidget0 = QWidget(self)
        self.viewWidget0.resize(self.frameSize())
        self.viewWidget0.setObjectName("viewWidget0")
        self.viewLayout0 = QVBoxLayout(self.viewWidget0)
        self.viewLayout0.setObjectName("viewLayout0")
        self.mot = QPushButton(card.word, self.viewWidget0)
        self.mot.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 18pt \"Arial Black\";")
        self.mot.setObjectName("mot")
        self.viewLayout0.addWidget(self.mot)
        self.viewWidget0.setVisible(False)
        # la face Infos
        self.viewWidget1 = QWidget(self)
        self.viewWidget1.resize(self.frameSize())
        self.viewWidget1.setObjectName("viewWidget0")
        self.viewLayout1 = QVBoxLayout(self.viewWidget1)
        self.viewLayout1.setObjectName("viewLayout0")
        self.description = QPushButton(card.shortStr(), self.viewWidget1)
        self.description.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 11pt \"Arial Black\";")
        self.description.setObjectName("description")
        self.viewLayout1.addWidget(self.description)
        self.viewWidget1.setVisible(False)
        #face Image
        #path=card.image
        path='images/image.jpg'
        if path == '':
            self.viewWidget2=None              #pas d'image fournie
        else:
            self.viewWidget2=QLabel(self)
            self.viewWidget2=self.viewWidget2
            self.viewWidget2.resize(self.frameSize().width()-100, self.frameSize().height()-60)
            self.pixmap=QtGui.QPixmap()
            
            self.pixmap.load(path)
            self.pixmap=self.pixmap.scaled(self.viewWidget2.frameSize().width(), self.viewWidget2.frameSize().height()-30, QtCore.Qt.KeepAspectRatio)
            self.viewWidget2.setPixmap(self.pixmap)
            self.viewWidget2.setScaledContents(True)
            self.viewWidget2.setVisible(False)

        ## affichage de la bonne face
        self.viewWidgets=[self.viewWidget0, self.viewWidget1, self.viewWidget2]
        self.viewNtools.addWidget(self.viewWidgets[self.currentview], 1, 1, 1, 1)
        self.viewWidgets[self.currentview].setVisible(True)

        # signaux et slots
        self.flipButton.clicked.connect(self.flipping)
        self.pictureButton.clicked.connect(self.flipPicture)
        self.modifInterf=None
        self.editButton.clicked.connect(self.openmodif)
        
    def alternateViews(self):
        self.viewNtools.removeWidget(self.viewWidgets[self.previousview])
        self.viewNtools.addWidget(self.viewWidgets[self.currentview], 1, 1, 1, 1)
        self.viewWidgets[self.previousview].setVisible(False)
        self.viewWidgets[self.currentview].setVisible(True)

    def flipping(self):
        self.previousview=self.currentview
        if self.previousview==0:    #face mot -> face carte
            self.currentview=1
        elif self.previousview==1 or self.previousview==2:    #face carte ou image -> face mot
            self.currentview=0    
        self.alternateViews()
       
    def flipPicture(self):
        if self.currentview==2:
            (self.previousview, self.currentview)=(self.currentview, self.previousview)
        else:
            self.previousview=self.currentview
            self.currentview=2
        self.alternateViews()

    deletedSignal=QtCore.pyqtSignal()
    modifiedSignal=QtCore.pyqtSignal()
    
    def openmodif(self):
        self.modifWindow = QWidget()
        self.modifWindow.setFixedSize(497, 492)
        self.modifInterf = createcardsInterf.CardModification(self.modifWindow, self.card)
        self.modifInterf.deleted.connect(self.deleted)
        self.modifInterf.modified.connect(self.modified)
        self.modifWindow.show()
        self.modifInterf.show()
        
    def deleted(self):
        self.modifWindow.close()
        self.deletedSignal.emit()
    
    def modified(self):
        self.modifWindow.close()
        self.modifiedSignal.emit()

class viewDialog(QWidget):
    def __init__(self, parentWindow, begin, givenCards):
        super(QWidget, self).__init__(parentWindow)
        self.setWindowTitle("Enjoy reading your FlashCard")
        self.resize(parentWindow.frameSize())
        # le nombre de cartes
        self.nbCard=len(givenCards)
        self.givenCards=givenCards
        # le widget de vue
        self.background = QWidget(self)
        self.background.resize(self.frameSize())
        self.background.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.background.setObjectName("background")
        #self.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        ### 3 lignes suivantes peut etre a enlever
        #self.horizontalLayoutWidget = QWidget(self.background)
        #self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 830, 480))
        #self.horizontalLayoutWidget.setObjectName("ReadingWidget")
        self.viewbar = QHBoxLayout(self.background)
        self.viewbar.setContentsMargins(0, 0, 0, 0)
        self.viewbar.setObjectName("viewbar")
        # le bouton precedent
        self.previous = QPushButton(u" ", self.background)
        self.previous.setMinimumSize(QtCore.QSize(71, 71))
        self.previous.setMaximumSize(QtCore.QSize(71, 71))
        self.previous.setStyleSheet("background-image: url(:/icons/previous.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.previous.setObjectName("previous")
        self.viewbar.addWidget(self.previous)
        # la carte
        self.cardnumber=begin
        self.cardWindow=QWidget(self.background)
        self.cardWindow.setMinimumSize(QtCore.QSize(361, 251))
        self.cardWindow.setMaximumSize(QtCore.QSize(361, 251))
        self.currentCard=CardWidget(self.givenCards[self.cardnumber],self.cardWindow)
        self.viewbar.addWidget(self.cardWindow)
        # le bouton suivant
        self.next = QtWidgets.QPushButton(u" ", self.background)
        self.next.setMinimumSize(QtCore.QSize(71, 71))
        self.next.setMaximumSize(QtCore.QSize(71, 71))
        self.next.setStyleSheet("background-image: url(:/icons/next.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.next.setObjectName("next")
        self.viewbar.addWidget(self.next)
        
        #shortcuts
        self.nextShortcut=QShortcut(QtGui.QKeySequence('Right'), self)
        self.prevShortcut=QShortcut(QtGui.QKeySequence('Left'), self)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.next.clicked.connect(self.toNextCard)
        self.previous.clicked.connect(self.toPreviousCard)
        self.nextShortcut.activated.connect(self.toNextCard)
        self.prevShortcut.activated.connect(self.toPreviousCard)
        self.currentCard.modifiedSignal.connect(self.currentCardWasModified)
        self.currentCard.deletedSignal.connect(self.currentCardWasDeleted)
        
    #fonction appelee apres modification de la carte 
    def currentCardWasModified(self):
        #on modifie la carte
        self.givenCards[self.cardnumber]=database.getCardById(self.givenCards[self.cardnumber].tablename, self.givenCards[self.cardnumber].name)
        #on reinitialise currentCard en gardant la meme vue
        view=self.currentCard.currentview
        self.currentCard.close()
        self.currentCard = CardWidget(self.givenCards[self.cardnumber], self.cardWindow, view)
        self.currentCard.show()
        #l'utilisateur peut voir les changements apportes a la carte
        
    #fonction appelee apres suppression de la carte
    def currentCardWasDeleted(self):
        del self.givenCards[self.cardnumber]
        
        self.nbCard-=1
        if (self.cardnumber==self.nbCard):
            self.toPreviousCard()
        else:
            self.cardnumber-=1
            self.toNextCard()

    def toNextCard(self):
        if self.cardnumber<self.nbCard-1:
            self.cardnumber += 1
            #changement de carte (dans l'ordre des noms) vers +1
            self.currentCard.close()
            self.currentCard = CardWidget(self.givenCards[self.cardnumber], self.cardWindow)
            self.currentCard.show()
            self.previous.setEnabled(True)
            self.currentCard.modifiedSignal.connect(self.currentCardWasModified)
            self.currentCard.deletedSignal.connect(self.currentCardWasDeleted)
        else:
            self.next.setEnabled(False)

    def toPreviousCard(self):
        if self.cardnumber>0:
            self.cardnumber -= 1
            #changement de carte (dans l'ordre des noms) vers -1
            self.currentCard.close()
            self.currentCard = CardWidget(self.givenCards[self.cardnumber], self.cardWindow)
            self.currentCard.show()
            self.next.setEnabled(True)
            self.currentCard.modifiedSignal.connect(self.currentCardWasModified)
            self.currentCard.deletedSignal.connect(self.currentCardWasDeleted)
        else:
            self.previous.setEnabled(False)
    
if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    AllCards = database.getAllCards('anglais')
    args = sys.argv
    b = QApplication(args)
    w = QWidget()
    #w.resize(830, 480)
    w.resize(1000, 600)
    mf = viewDialog(w, 0, AllCards)
    w.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
