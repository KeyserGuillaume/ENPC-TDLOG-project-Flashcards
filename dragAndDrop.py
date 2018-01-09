# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel
import sys
import database
from random import randrange


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
    database.modifyCard(card.tablename, card.name, card.trad, card.exemple, card.thema, card.howhard, card.level, card.image, card.prononciation, card.nature)
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
    error=QtCore.pyqtSignal()
    success=QtCore.pyqtSignal()

    # event on veut bouger la carte
    def mouseMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        text=self.text()+';'+('%d,%d' % (event.x(), event.y()))
        mimeData.setText(text)
        #make a transparent button be dragged by the pointer
        b=QtCore.QCoreApplication.instance ()
        pixmap = QtGui.QScreen.grabWindow(b.primaryScreen(),self.winId())
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
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
            if self.text()=="GAME OVER" or self.text()=="TIME IS OUT":
                event.ignore()
                e.source().setDown(False)
                return
            if match(cardSource.text(),self.text()) or match(self.text(),cardSource.text()) :
                event.acceptProposedAction()
                #self.move(event.pos())
                #cardSource.move(event.pos())                
                self.success.emit()
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
                self.error.emit()
                event.ignore()
        else:
            event.ignore()

### le widget de jeu (cartes aleatoires qui se droppent et layout de droppage)
class DragDropGame(QWidget):
    def __init__(self,bigWindow, CardsPlayed):
        ## la fenetre
        super(DragDropGame, self).__init__(bigWindow)
        self.setObjectName("Jeu de reliage")
        self.setWindowTitle("Drag and Drop")
        self.resize(833, 423)
        self.setAcceptDrops(True)
        ## les futures listes de boutons
        self.myCards = []
        self.myTrads = []
        ## le layout pour mettre les cartes jouees
        self.doneWidget = QWidget(self)
        self.doneWidget.setGeometry(QtCore.QRect(590, 10, 228, 401))
        self.doneWidget.setObjectName("Bien joué")
        self.Welldone = QVBoxLayout(self.doneWidget)
        self.Welldone.setAlignment(QtCore.Qt.AlignTop)
        self.Welldone.setObjectName("Welldone")
        ## l'ajout de tous les boutons concernés (maitrise < ...)
        for i,carte in enumerate(CardsPlayed) :
            self.myCards.append(ButtonToDrag(carte,'mot', self, self.Welldone))
            myx=randrange(5,470,1)
            myy=randrange(5,390,1)
            self.myCards[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myCards[i].error.connect(self.error.emit)
            self.myCards[i].success.connect(self.success.emit)
            self.myTrads.append(ButtonToDrag(carte,'trad', self, self.Welldone))
            myx = randrange(5, 520, 1)
            myy = randrange(5, 380, 1)
            self.myTrads[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myTrads[i].error.connect(self.error.emit)
            self.myTrads[i].success.connect(self.success.emit)
        #le message de victoire
        self.victoryWidget=QWidget(self)
        self.victoryWidget.resize(300, 200)
        qr=self.victoryWidget.frameGeometry()
        qr.moveCenter(self.rect().center())
        self.victoryWidget.move(qr.topLeft())
        self.label=QLabel(self.victoryWidget)
        path="icons/victory.png"
        self.pixmap=QtGui.QPixmap()
        self.pixmap.load(path)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True) 
        self.victoryWidget.setVisible(False) 
    error=QtCore.pyqtSignal()
    success=QtCore.pyqtSignal()
    
    def dragEnterEvent(self, e):
        e.accept()
        
    def dropEvent(self, e):
        mime = e.mimeData().text()
        mime = (mime.split(';'))[1]
        x, y = map(int, mime.split(','))
        e.source().move(e.pos()-QtCore.QPoint(x, y))
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        e.source().setDown(False)

    #### il faut bouger un bouton sur un autre
    #### la classe ButtonToDrag gere les events

from time import time, strftime,localtime


class GameWindow (QWidget):
    def __init__(self, CartesJouees):
        super(QWidget, self).__init__()
        print(len(CartesJouees))
        self.myCards=CartesJouees
        self.initGame()
    def initGame(self):
        self.nberreurs=0
        self.nbSucces=0
        self.t0=time()
        self.timeGiven=60
        ## la fenetre
        self.setObjectName("Jeu de reliage")
        self.setWindowTitle("Drag and Drop")
        self.setFixedSize(853, 554)
        ## le jeu comme defini ci dessus
        self.theGame=DragDropGame(self, self.myCards)
        self.theGame.error.connect(self.incrementErrorCount)
        self.theGame.success.connect(self.incrementSuccessCount)
        ## la barre de boutons/compteurs du bas
        self.BottomWidget = QWidget(self)
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
        self.resetButton.clicked.connect(self.reset)
        self.GameBox.addWidget(self.resetButton)
        # compteur chrono
        self.chrono = QLCDNumber(self.BottomWidget)
        self.chrono.setDigitCount(2)
        self.chrono.setObjectName("chrono")
        self.GameBox.addWidget(self.chrono)
        self.timer = QtCore.QTimer(self)
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
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.Mistake)
        self.timer2.start(10)
        self.GameBox.addWidget(self.failure)
        
    def incrementSuccessCount(self):
        self.nbSucces+=1;
        if (self.nbSucces==1):#len(self.myCards)):
            print("ok")
            self.theGame.victoryWidget.setVisible(True)
        
    def incrementErrorCount(self):
        self.nberreurs+=1
    def Time(self):
        if (self.nbSucces==len(self.myCards)):
            return
        #currenttime = time()-t0
        # affiche l'heure
        # regarder doc de time pour changer en un chrono descendant
        timeLeft=self.timeGiven-(time()-self.t0)//1
        if (timeLeft<0) :
            self.timeIsOut()
            return
        self.chrono.display(timeLeft)
        #self.chrono.display(strftime("%H" + ":" + "%M" + ":" + "%S", localtime()))
    def timeIsOut(self):
        for carte in self.theGame.myCards:
            carte.setText('TIME IS OUT')
        for carte in self.theGame.myTrads:
            carte.setText('GAME OVER')
    def reset(self):
        self.theGame.close()
        self.BottomWidget.close()
        self.initGame()
        self.theGame.show()
        self.BottomWidget.show()
        self.theGame.victoryWidget.setVisible(False)
    def Mistake(self):
        self.failure.display(self.nberreurs)



if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)
    args = sys.argv
    b = QApplication(args)
    mf = GameWindow(CartesEnJeu)
    mf.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
