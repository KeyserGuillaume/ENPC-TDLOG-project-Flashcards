from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QShortcut, QLCDNumber, QLabel
import sys
from model import database, rechercheFonct
from view.games import gameWindow, dragAndDrop
from view import parcours
from random import randrange

class hotColdGameWindow(QWidget):
    def __init__(self, parentWindow, cardPlayed):
        super(hotColdGameWindow, self).__init__(parentWindow)
        self.resize(parentWindow.frameSize())
        self.layout=QGridLayout(self)
        self.currentCard=cardPlayed
        parentWindow.setStyleSheet("background-image: url(:/fond/silver.jpg);")
        #on met n'importe quoi pour rank parce qu'on n'en aura pas besoin
        #cardlist : on a encore besoin de cet argument ?
        self.card=parcours.CardButton(self.currentCard, 0, [], self, self.frameSize().width()/5)
        self.layout.addWidget(self.card, 0, 0, 1, 1)
        self.editWidget=QWidget()
        self.editWidget.setFixedSize(self.card.frameSize())
        self.lineEdit=QLineEdit(self.editWidget)
        self.editWidgetLayout=QVBoxLayout(self.editWidget)
        self.editWidgetLayout.addWidget(self.lineEdit)
        #self.lineEdit.resize(self.frameSize().width()/5, self.lineEdit.frameSize().height())
        self.layout.addWidget(QWidget(), 1, 0, 1, 1)
        self.layout.addWidget(self.editWidget, 2, 0, 1, 1)
        self.confirmShortcut=QShortcut(QtGui.QKeySequence('Return'), self.lineEdit, self.checkAnswer)
        self.lineEdit.setFocus(True)

        #l'echelle : un degrade bleu -rouge
        self.degradeWidget=QLabel(self)
        self.degradeWidget=self.degradeWidget
        self.degradeWidget.resize(self.frameSize().width()*0.5, 35)
        self.pixmap=QtGui.QPixmap()
        path="icons/gradient.jpg"
        self.pixmap.load(path)
        self.pixmap=self.pixmap.scaled(self.degradeWidget.frameSize().width(), self.degradeWidget.frameSize().height()-30, QtCore.Qt.KeepAspectRatio)
        self.degradeWidget.setPixmap(self.pixmap)
        self.degradeWidget.setScaledContents(True)
        #on met une fenetre vide pour reserver de la place
        self.emptyWidget=QWidget(self)
        self.emptyWidget.setVisible(False)
        self.emptyWidget.setFixedSize(20, self.frameSize().height()*0.4)
        self.layout.addWidget(self.emptyWidget, 3, 0, 60, 1)
        #positionnement du degrade
        self.degradeWidget.move(self.frameSize().width()*0.5-self.degradeWidget.frameSize().width()*0.5, self.frameSize().height()*0.65)
        
        #un pointeur en-dessous du degrade
        self.pointeurWidget=QLabel(self)
        self.pointeurWidget=self.pointeurWidget
        self.pointeurWidget.resize(45, 56)
        self.pixmap=QtGui.QPixmap()
        path="icons/fleche.png"
        self.pixmap.load(path)
        self.pointeurWidget.setPixmap(self.pixmap)
        #position initiale du pointeur
        self.leftMostPos=self.frameSize().width()*0.5-self.pointeurWidget.frameSize().width()*0.5-self.degradeWidget.frameSize().width()*0.5
        self.rightMostPos=self.frameSize().width()*0.5-self.pointeurWidget.frameSize().width()*0.5+self.degradeWidget.frameSize().width()*0.5  
        self.currentPointerPosition=self.leftMostPos
        self.currentPointerSpeed=0
        self.currentPointerTarget=self.currentPointerPosition
        self.pointeurWidget.move(self.currentPointerPosition, self.frameSize().height()*0.76)
        
        #timer pour mouvement fluide du pointeur
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.movePointer)
        self.timer.start(10)
        
        self.lineEdit.textEdited.connect(self.definePointerTarget)
        
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
        
        #le message de defaite
        self.defeatWidget=QWidget(self)
        self.defeatWidget.resize(300, 200)
        qr=self.defeatWidget.frameGeometry()
        qr.moveCenter(self.rect().center())
        self.defeatWidget.move(qr.topLeft())
        self.label=QLabel(self.defeatWidget)
        path="icons/gameOver.png"
        self.pixmap=QtGui.QPixmap()
        self.pixmap.load(path)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True) 
        self.defeatWidget.setVisible(False)
    error=QtCore.pyqtSignal()
    success=QtCore.pyqtSignal()
    def definePointerTarget(self):
        difference=rechercheFonct.DistanceDeDamerauLevenshtein(self.currentCard.trad, self.lineEdit.displayText())
        percentCorrespond=difference/len(self.currentCard.trad)
        self.currentPointerTarget=self.leftMostPos+max(len(self.currentCard.trad)-difference, 0)*self.degradeWidget.frameSize().width()/len(self.currentCard.trad)
    def movePointer(self):
        self.currentPointerSpeed=0.01*(self.currentPointerTarget-self.currentPointerPosition)
        self.currentPointerPosition+=self.currentPointerSpeed
        self.pointeurWidget.move(self.currentPointerPosition, self.frameSize().height()*0.76)
    def checkAnswer(self):
        if (dragAndDrop.match(self.currentCard.word, self.lineEdit.displayText(), self.currentCard.tablename)):
            self.success.emit()
        else:
            self.error.emit()
    def displayFirstCharacters(self, nbChar):
        self.lineEdit.setText(self.currentCard.trad[0:nbChar])
    def onVictory(self):
        self.degradeWidget.hide()
        self.victoryWidget.show()
    def onDefeat(self):
        self.degradeWidget.hide()
        self.defeatWidget.show()
    

class Game(QWidget):
    def __init__(self, parentWindow, cardsPlayed):
        super(pointToGame,  self).__init__(parentWindow)
        self.resize(givenWindow.frameSize())
        self.cartesJouables=cardsPlayed
        self.init()

class hotColdGame(QWidget):
    def __init__(self, givenWindow, cardsPlayed):
        super(hotColdGame, self).__init__(givenWindow)
        self.resize(givenWindow.frameSize())
        self.cartesJouables=cardsPlayed
        self.nbCharsDisplayed=0
        self.init()
    leave=QtCore.pyqtSignal()
    def init(self):
        self.cartesJouees=[]
        while (len(self.cartesJouees)<10 and not len(self.cartesJouees)==len(self.cartesJouables)):
            i=randrange(0, len(self.cartesJouables))
            if (self.cartesJouables[i] not in self.cartesJouees):
                self.cartesJouees.append(self.cartesJouables[i])
        self.window=gameWindow.GameWindow(self, len(self.cartesJouees))
        self.game=hotColdGameWindow(self.window.gameArea, self.cartesJouees[0])
        self.currentCardNb=0;
        self.window.show()
        
        self.window.resetSignal.connect(self.reset)
        self.window.leaveSignal.connect(self.endOfGame)
        self.game.error.connect(self.onFailure)
        self.game.success.connect(self.onSuccess)
        self.window.timeIsOut.connect(self.game.onDefeat)
    def onFailure(self):
        self.window.incrementErrorCount()
        self.nbCharsDisplayed+=1
        self.game.displayFirstCharacters(self.nbCharsDisplayed)
        self.game.definePointerTarget()
    def onSuccess(self):
        self.window.incrementSuccessCount()
        self.nbCharsDisplayed=0
        if (self.currentCardNb<len(self.cartesJouees)-1):
            self.game.close()
            self.currentCardNb+=1
            self.game=hotColdGameWindow(self.window.gameArea, self.cartesJouees[self.currentCardNb])
            self.game.error.connect(self.onFailure)
            self.game.success.connect(self.onSuccess)
            self.window.gameWon.connect(self.game.onVictory)
            self.game.show()
    def reset(self):
        self.game.close()
        #la ligne suivante evite que la fenetre, meme fermee, envoie le signal timeIsOut
        self.window.timeIsOut.disconnect()
        self.window.close()
        self.init()
    def endOfGame(self):
        self.leave.emit()
        self.close()


'''
if __name__ == "__main__":
    Table='anglais'
    ### cartes concernées par le jeu
    CartesEnJeu=database.getCardsToLearn(Table,0,9)
    args = sys.argv
    b = QApplication(args)
    w = QWidget()
    #w.resize(853, 554)
    w.resize(800, 400)#on peut modifier
    mf = hotColdGame(w, CartesEnJeu)
    w.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
'''