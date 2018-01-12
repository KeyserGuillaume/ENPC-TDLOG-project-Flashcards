# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel
import sys
import database
import gameWindow
from random import randrange


#### match (meme carte) entre mot et trad dans cet ordre
def match(text1, text2, language):
    answer=False
    matching=database.getCompleteCardsWithAttribute(language, 'mot', text1)
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
        self.language=card.tablename
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
            if match(cardSource.text(),self.text(), self.language) or match(self.text(),cardSource.text(), self.language) :
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
class dragDropGameWindow(QWidget):
    def __init__(self,bigWindow, CardsPlayed):
        ## la fenetre de jeux
        super(dragDropGameWindow, self).__init__(bigWindow)
        self.setObjectName("Jeu de reliage")
        self.setWindowTitle("Drag and Drop")
        self.resize(bigWindow.frameSize())
        self.width=self.frameSize().width()
        self.height=self.frameSize().height()
        #self.resize(833, 423)
        self.setAcceptDrops(True)
        ## les futures listes de boutons
        self.myCards = []
        self.myTrads = []
        ## le layout pour mettre les cartes jouees
        self.doneWidget = QWidget(self)
        self.doneWidget.setGeometry(QtCore.QRect(3/4*self.width-10, 10, 1/4*self.width, self.height))
        #self.doneWidget.setGeometry(QtCore.QRect(590, 10, 228, 401))
        self.doneWidget.setObjectName("Bien joué")
        self.Welldone = QVBoxLayout(self.doneWidget)
        self.Welldone.setAlignment(QtCore.Qt.AlignTop)
        self.Welldone.setObjectName("Welldone")
        ## l'ajout de tous les boutons concernés (maitrise < ...)
        for i,carte in enumerate(CardsPlayed) :
            self.myCards.append(ButtonToDrag(carte,'mot', self, self.Welldone))
            #myx=randrange(5,470,1)
            myx=randrange(5, int(3/4*self.width-150), 1)
            #myy=randrange(5,390,1)
            myy=randrange(5, int(3/4*self.height), 1)
            self.myCards[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myCards[i].error.connect(self.error.emit)
            self.myCards[i].success.connect(self.success.emit)
            self.myTrads.append(ButtonToDrag(carte,'trad', self, self.Welldone))
            #myx = randrange(5, 520, 1)
            myx=randrange(5, int(3/4*self.width-115), 1)
            #myy = randrange(5, 380, 1)
            myy=randrange(5, int(3/4*self.height), 1)
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

class dragDropGame(QWidget):
    def __init__(self, givenWindow, cardsPlayed):
        super(dragDropGame, self).__init__(givenWindow)
        self.resize(givenWindow.frameSize())
        self.cartesJouables=cardsPlayed
        self.init()
    leave=QtCore.pyqtSignal()
    def init(self):
        self.cartesJouees=[]
        while (len(self.cartesJouees)<10):
            i=randrange(0, len(self.cartesJouables))
            if (self.cartesJouables[i] not in self.cartesJouees):
                self.cartesJouees.append(self.cartesJouables[i])
        self.window=gameWindow.GameWindow(self, len(self.cartesJouees))
        self.game=dragDropGameWindow(self.window.gameArea, self.cartesJouees)
        self.window.show()
        
        self.window.resetSignal.connect(self.reset)
        self.window.leaveSignal.connect(self.endOfGame)
        self.game.error.connect(self.window.incrementErrorCount)
        self.game.success.connect(self.window.incrementSuccessCount)
        self.window.gameWon.connect(self.game.victoryWidget.show)
        self.window.timeIsOut.connect(self.timeIsOut)
    def reset(self):
        self.game.close()
        #la ligne suivante evite que la fenetre, meme fermee, envoie le signal timeIsOut
        self.window.timeIsOut.disconnect()
        self.window.close()
        self.init()
    def timeIsOut(self):
        for carte in self.game.myCards:
            carte.setText('TIME IS OUT')
        for carte in self.game.myTrads:
            carte.setText('GAME OVER')
    def endOfGame(self):
        self.leave.emit()
        self.close()
    
if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)
    args = sys.argv
    b = QApplication(args)
    w = QWidget()
    #w.resize(853, 554)
    w.resize(1000, 600)#on peut modifier
    mf = dragDropGame(w, CartesEnJeu)
    w.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)