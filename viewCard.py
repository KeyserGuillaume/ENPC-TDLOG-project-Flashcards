
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
import sys

import database


#### attention gestion de AllCards et NbCard va changer
## car problemes de "out of range" quand on change la base de données après ouverture d'une interface
## a gerer

## a lier au layout du cote de interfaccueil mais avec AllCard defini differemment

AllCard=database.getAllCards('anglais')
nbCard=len(AllCard)

from icons import icons
# permet l'accès aux images des icones

class CardWidget(QWidget):
    def __init__(self, card, place):
        super(CardWidget, self).__init__(place)
        # sauvegarde des données de la carte pour le flip
        self.card=card
        # les caractéristiques du widget de la carte
        self.setMinimumSize(QtCore.QSize(361, 270))
        self.setMaximumSize(QtCore.QSize(361, 270))
        self.setStyleSheet("background-image: url(:/fond/notebook.jpg);\n" "background-color: rgba(255, 231, 172, 128);")
        self.setObjectName("Card")
        #self.viewNtoolsWidget = QtWidgets.QWidget(self)
        #self.viewNtoolsWidget.setGeometry(QtCore.QRect(-1, 0, 361, 251))
        #self.viewNtoolsWidget.setObjectName("viewNtoolsWidget")
        # le layout separant contenu et outils
        self.viewNtools = QVBoxLayout(self)
        self.viewNtools.setContentsMargins(0, 0, 0, 0)
        self.viewNtools.setObjectName("viewNtools")
        # la carte
        self.cardButton = QPushButton(card.word,self)
        self.cardButton.setMinimumSize(QtCore.QSize(361, 230))
        self.cardButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n" "font: 18pt \"Arial\";")
        self.cardButton.setObjectName("cardButton")
        self.viewNtools.addWidget(self.cardButton)
        # la barre d'outil
        self.ToolsWidget = QWidget(self)
        self.ToolsWidget.setGeometry(QtCore.QRect(0, 0, 361, 32))
        self.ToolsWidget.setObjectName("ToolsWidget")
        self.ToolsLayout = QHBoxLayout(self.ToolsWidget)
        self.ToolsLayout.setObjectName("ToolsLayout")
        # zone vide
        spacerItem = QSpacerItem(40, 32, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ToolsLayout.addItem(spacerItem)
        # bouton edit
        self.editButton = QPushButton(u" ", self.ToolsWidget)
        self.editButton.setMinimumSize(QtCore.QSize(31, 32))
        self.editButton.setMaximumSize(QtCore.QSize(31, 32))
        self.editButton.setStyleSheet("background-image: url(:/icons/edit.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.editButton.setObjectName("editButton")
        self.ToolsLayout.addWidget(self.editButton)
        # bouton flip
        self.flipButton = QPushButton(u" ", self.ToolsWidget)
        self.flipButton.setMinimumSize(QtCore.QSize(41, 32))
        self.flipButton.setMaximumSize(QtCore.QSize(41, 32))
        self.flipButton.setStyleSheet("background-image: url(:/icons/flip.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.flipButton.setObjectName("flipButton")
        self.ToolsLayout.addWidget(self.flipButton)
        self.viewNtools.addWidget(self.ToolsWidget)
        #self.viewNtools.addLayout(self.ToolsLayout)


class ViewDialog(object):
    def __init__(self, begin):
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
        self.currentCard=CardWidget(AllCard[self.cardnumber],self.background)
        self.viewbar.addWidget(self.currentCard)
        # le bouton suivant
        self.next = QtWidgets.QPushButton(u" ", self.background)
        self.next.setMinimumSize(QtCore.QSize(71, 71))
        self.next.setMaximumSize(QtCore.QSize(71, 71))
        self.next.setStyleSheet("background-image: url(:/icons/next.png);\n" "background-color: rgba(255, 255, 255, 0);")
        self.next.setObjectName("next")
        self.viewbar.addWidget(self.next)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.next.clicked.connect(self.tonextcard)
        self.previous.clicked.connect(self.topreviouscard)

    def tonextcard(self):
        global nbCard
        if self.cardnumber<nbCard-1:
            self.cardnumber += 1
            #changement de carte (dans l'ordre des noms) vers +1
            self.viewbar.removeWidget(self.currentCard)
            self.currentCard = CardWidget(AllCard[self.cardnumber], self.background)
            self.viewbar.insertWidget(1,self.currentCard)
            self.previous.setEnabled(True)
        else:
            self.next.setEnabled(False)

    def topreviouscard(self):
        if self.cardnumber>0:
            self.cardnumber -= 1
            #changement de carte (dans l'ordre des noms) vers -1
            self.viewbar.removeWidget(self.currentCard)
            self.currentCard = CardWidget(AllCard[self.cardnumber], self.background)
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
    mf = ViewDialog(0)
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
