from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout, QLabel
import sys

import database, createcardsInterf


## a lier au layout du cote de interfaccueil

from icons import icons
# permet l'accès aux images des icones


### pour l'instant un probleme inconnu limite a un seul flip visuel par carte -> Pb regle

class CardWidget(QWidget):
    def __init__(self, card, place):
        super(CardWidget, self).__init__(place)
        # sauvegarde des donnees de la carte pour le flip
        self.card=card
        # la face affichee
        ### petit probleme avec de l'affichage laminaire en changent de face (widgets, ...)
        self.currentview=0
        # les caracteristiques du widget de la carte
        self.setMinimumSize(QtCore.QSize(361, 251))
        self.setMaximumSize(QtCore.QSize(361, 251))
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);")
        self.setObjectName("Card")
        # le layout separant contenu et outils
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 361, 251))
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
        self.viewWidget0.setGeometry(QtCore.QRect(361, 0, 288, 186))
        self.viewWidget0.setObjectName("viewWidget0")
        self.viewLayout0 = QVBoxLayout(self.viewWidget0)
        self.viewLayout0.setObjectName("viewLayout0")
        self.mot = QPushButton(card.word, self.viewWidget0)
        self.mot.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 18pt \"Arial Black\";")
        self.mot.setObjectName("mot")
        self.viewLayout0.addWidget(self.mot)
        # la face Infos
        self.viewWidget1 = QWidget(self)
        self.viewWidget1.setGeometry(QtCore.QRect(361, 0, 288, 186))
        self.viewWidget1.setObjectName("viewWidget0")
        self.viewLayout1 = QVBoxLayout(self.viewWidget1)
        self.viewLayout1.setObjectName("viewLayout0")
        self.description = QPushButton(card.__str__(), self.viewWidget1)
        self.description.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 11pt \"Arial Black\";")
        self.description.setObjectName("description")
        self.viewLayout1.addWidget(self.description)
        # code precedent, je ne sais pas s'il est utile, mais je n'ai pas voulu le supprimer
#        self.viewWidget1 = QWidget(self)
#        self.viewWidget1.setGeometry(QtCore.QRect(361, 0, 288, 186))
#        self.viewWidget1.setObjectName("viewWidget1")
#        self.viewLayout1 = QVBoxLayout(self.viewWidget1)
#        self.viewLayout1.setObjectName("viewLayout1")
#        self.trad = QPushButton(card.trad, self.viewWidget1)
#        self.trad.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 87 18pt \"Arial Black\";")
#        self.trad.setObjectName("trad")
#        self.viewLayout1.addWidget(self.trad)
#        self.nature = QPushButton(card.nature, self.viewWidget1)
#        self.nature.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: italic 13pt \"Arial Narrow\";")
#        self.nature.setObjectName("nature")
#        self.viewLayout1.addWidget(self.nature)
#        viewexemple = "exemple : "+ card.exemple
#        self.exemple = QPushButton(viewexemple, self.viewWidget1)
#        self.exemple.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 18pt \"Arial\";")
#        self.exemple.setObjectName("exemple")
#        self.viewLayout1.addWidget(self.exemple)
#        viewautre = "in : " + card.thema + ", "+ card.tablename + " ; niveau : " + str(card.howhard) + " ; ..."
#        self.autre = QPushButton(viewautre, self.viewWidget1)
#        self.autre.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 14pt \"Arial\";")
#        self.autre.setObjectName("autre")
#        self.viewLayout1.addWidget(self.autre)

        ## affichage de la bonne face
        if self.currentview==0:
            self.viewNtools.addWidget(self.viewWidget0, 1, 1, 1, 1)
        else:
            self.viewNtools.addWidget(self.viewWidget1, 1, 1, 1, 1)

        # signaux et slots
        self.flipButton.clicked.connect(self.flipping)
        self.modifInterf=None
        self.editButton.clicked.connect(self.openmodif)

    def flipping(self):
        if self.currentview==0:
            self.currentview=1
            # changement de cote
            self.viewNtools.removeWidget(self.viewWidget0)
            self.viewNtools.addWidget(self.viewWidget1, 1, 1, 1, 1)
            self.viewWidget0.setVisible(False)
            self.viewWidget1.setVisible(True)
            print("flip", self.currentview)
        else:
            self.currentview=0
            # changement de cote
            self.viewNtools.removeWidget(self.viewWidget1)
            self.viewNtools.addWidget(self.viewWidget0, 1, 1, 1, 1)
            self.viewWidget1.setVisible(False)
            self.viewWidget0.setVisible(True)
            print("flip", self.currentview)

    def openmodif(self):
        self.modifInterf = createcardsInterf.CardModification(self.card)
        self.modifInterf.show()


class ViewDialog(object):
    def __init__(self, begin, givenCards):
        # le nombre de cartes
        self.nbCard=len(givenCards)
        self.givenCards=givenCards
        # la fenetre
        self.Dialog = QWidget()
        self.Dialog.setObjectName("View")
        self.Dialog.setWindowTitle("Enjoy reading your FlashCard")
        self.Dialog.resize(830, 480)
        # le widget de vue
        self.background = QWidget(self.Dialog)
        self.background.setGeometry(QtCore.QRect(0, 0, 830, 480))
        self.background.setStyleSheet("background-image: url(:/fond/blackboard.jpg);")
        self.background.setObjectName("background")
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
        self.currentCard=CardWidget(givenCards[self.cardnumber],self.background)
        self.viewbar.addWidget(self.currentCard)
        # le bouton suivant
        self.next = QtWidgets.QPushButton(u" ", self.background)
        self.next.setMinimumSize(QtCore.QSize(71, 71))
        self.next.setMaximumSize(QtCore.QSize(71, 71))
        self.next.setStyleSheet("background-image: url(:/icons/next.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.next.setObjectName("next")
        self.viewbar.addWidget(self.next)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.next.clicked.connect(self.toNextCard)
        self.previous.clicked.connect(self.toPreviousCard)

    def toNextCard(self):
        if self.cardnumber<self.nbCard-1:
            self.cardnumber += 1
            #changement de carte (dans l'ordre des noms) vers +1
            self.viewbar.removeWidget(self.currentCard)
            self.currentCard = CardWidget(self.givenCards[self.cardnumber], self.background)
            self.viewbar.insertWidget(1,self.currentCard)
            self.previous.setEnabled(True)
        else:
            self.next.setEnabled(False)

    def toPreviousCard(self):
        if self.cardnumber>0:
            self.cardnumber -= 1
            #changement de carte (dans l'ordre des noms) vers -1
            self.viewbar.removeWidget(self.currentCard)
            self.currentCard = CardWidget(self.givenCards[self.cardnumber], self.background)
            self.viewbar.insertWidget(1, self.currentCard)
            self.next.setEnabled(True)
        else:
            self.previous.setEnabled(False)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()

def main():
    args = sys.argv
    a = QApplication(args)
    AllCard = database.getAllCards('anglais')
    mf = ViewDialog(0, AllCard)
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
