from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber
import sys
import database
from random import randrange

Table='anglais'
### cartes concernées par le jeu
CartesEnJeu=database.getCardsToLearn(Table,0,9)
#ListCartesEnJeu=["suspendre","remuer","amour","bonjour","douche","rideau","empreinte","carafe"]
#ListTradsEnJeu=["sling","dwell","love","hello","shower","curtain","mark","carafe"]

## variable globale comptant les erreurs
nberreurs=0

#### match (meme carte) entre mot et trad dans cet ordre
def match(text1,text2):
    answer=False
    matching=database.getCompleteCardsWithAttribute('anglais', 'mot', text1)
    for card in matching:
        answer = answer or (text2==card.trad)
    return answer

## baisse de un la maitrise dans la carte et la base
def downgradeLevel(card):
    card._level -= 1
    database.modifyCard(Table, card.name, card.trad, card.exemple, card.thema, card.howhard, card.level, card.image, card.prononciation, card.nature)
    #print("maitrise moins")

### la classe de bouton qui se drop
class ButtonToDrag(QPushButton):
    def __init__(self, card, type, place, depot):
        self.lacarte=card
        if type=='mot':
            super(ButtonToDrag, self).__init__(card.word, place)
        else: #pour l'instant que 2 types donc trad
            super(ButtonToDrag, self).__init__(card.trad, place)
            self.setStyleSheet("background-color: rgb(122, 227, 255);\n" "border-color: rgb(0, 0, 0);\n" "font: 75 13pt \"Helvetica Neue\";")
        self.setAcceptDrops(True)
        self.jouees=depot

    # event on veut bouger la carte
    def mouseMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(QtCore.Qt.MoveAction)
        #print("moving...")

    # event on a bougé la carte sur une autre carte
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            #print("dragging... ")
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            cardSource = event.source()
            #print("droping...")
            # bouge les 2 cartes dans le layout sur le cote si elles coincident
            if match(cardSource.text(),self.text()) or match(self.text(),cardSource.text()) :
                event.acceptProposedAction()
                #self.move(event.pos())
                #cardSource.move(event.pos())
                horizontalLayout = QHBoxLayout()
                horizontalLayout.setAlignment(QtCore.Qt.AlignTop)
                horizontalLayout.setObjectName("Mon coup")
                horizontalLayout.addWidget(cardSource)
                horizontalLayout.addWidget(self)
                self.jouees.addLayout(horizontalLayout)
                event.accept()
            else:
                # mise a jour de la maitrise des cartes
                if self.lacarte.level >= 1:
                    downgradeLevel(self.lacarte)
                if cardSource.lacarte.level >= 1:
                    downgradeLevel(cardSource.lacarte)
                # mise a jour du decompte d'erreurs
                global nberreurs
                nberreurs += 1
                event.ignore()
        else:
            event.ignore()

### le widget de jeu (cartes aleatoires qui se droppent et layout de droppage)
class DragDropGame(object):
    def __init__(self,bigWindow):
        ## la fenetre
        self.Dialog = QWidget(bigWindow)
        self.Dialog.setObjectName("Jeu de reliage")
        self.Dialog.setWindowTitle("Drag and Drop")
        self.Dialog.resize(833, 423)
        ## les futures listes de boutons
        self.myCards = CartesEnJeu
        self.myTrads = CartesEnJeu
        ## le layout pour mettre les cartes jouees
        self.doneWidget = QWidget(self.Dialog)
        self.doneWidget.setGeometry(QtCore.QRect(590, 10, 228, 401))
        self.doneWidget.setObjectName("Bien joué")
        self.Weldone = QVBoxLayout(self.doneWidget)
        self.Weldone.setAlignment(QtCore.Qt.AlignTop)
        self.Weldone.setObjectName("Weldone")
        ## l'ajout de tous les boutons concernés (maitrise < ...)
        for i,carte in enumerate(CartesEnJeu) :
            self.myCards[i]=ButtonToDrag(carte,'mot', self.Dialog, self.Weldone)
            myx=randrange(5,470,1)
            myy=randrange(5,390,1)
            self.myCards[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myTrads[i] = ButtonToDrag(carte,'trad', self.Dialog, self.Weldone)
            myx = randrange(5, 520, 1)
            myy = randrange(5, 380, 1)
            self.myTrads[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))

    #### il faut bouger un bouton sur un autre
    #### la classe ButtonToDrag gere les events

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def close(self):
        self.Dialog.close()

from time import time, strftime,localtime

t0=time()

class GameWindow (object):
    def __init__(self):
        ## la fenetre
        self.Dialog = QWidget()
        self.Dialog.setObjectName("Jeu de reliage")
        self.Dialog.setWindowTitle("Drag and Drop")
        self.Dialog.setFixedSize(853, 554)
        ## le jeu comme defini ci dessus
        self.theGame=DragDropGame(self.Dialog)
        ## la barre de boutons/compteurs du bas
        self.BottomWidget = QWidget(self.Dialog)
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
        self.GameBox.addWidget(self.resetButton)
        # compteur chrono
        self.chrono = QLCDNumber(self.BottomWidget)
        self.chrono.setDigitCount(8)
        self.chrono.setObjectName("chrono")
        self.GameBox.addWidget(self.chrono)
        self.timer = QtCore.QTimer(self.Dialog)
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
        self.timer2 = QtCore.QTimer(self.Dialog)
        self.timer2.timeout.connect(self.Mistake)
        self.timer2.start(10)
        self.GameBox.addWidget(self.failure)

    def Time(self):
        #currenttime = time()-t0
        # affiche l'heure
        # regarder doc de time pour changer en un chrono descendant
        self.chrono.display(strftime("%H" + ":" + "%M" + ":" + "%S", localtime()))
    def Mistake(self):
        self.failure.display(nberreurs)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def close(self):
        self.Dialog.close()

if __name__ == "__main__":
    args = sys.argv
    b = QApplication(args)
    mf = GameWindow()
    mf.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
