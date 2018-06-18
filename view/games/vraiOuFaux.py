# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel, QMessageBox
import sys, random
from model import database
from view.games import gameWindow
from view import AccessSettings
from random import randrange, randint

#### match (meme carte) entre mot et trad dans cet ordre
def match(text1,text2,cartesJouables):
    answer=False
    matching = []
    for item in cartesJouables:
        if item.word == text1:
            matching.append(item)
    for card in matching:
        answer = answer or (text2==card.trad)
    return answer


def getTradRandom(carte, cartesJouables):
    cardsSameNature = []
    result = []
    result.append(carte.word)
    i=random.randint(0,1)
    if i == 0:
        result.append(carte.trad)
    elif i == 1:
        for item in cartesJouables:
            if item.nature == carte.nature:
                cardsSameNature.append(item)
        if carte.nature != '' and len(cardsSameNature) != 0:
            j = random.randint(0, len(cardsSameNature)-1)
            result.append(cardsSameNature[j].trad)
        else:
            j = random.randint(0, len(cartesJouables)-1)
            result.append(cartesJouables[j].trad)
    return result



class vraiFauxGameWindow(QWidget):
    def __init__(self,bigWindow, cartesJouees, cartesJouables):
        ## la fenetre de jeux
        super(vraiFauxGameWindow, self).__init__(bigWindow)
        self.cartesJouees = cartesJouees
        self.cartesJouables = cartesJouables
        self.setObjectName("VraiOUFaux")
        self.setWindowTitle("Vrai OU Faux")
        self.resize(bigWindow.frameSize())
        self.width=self.frameSize().width()
        self.height=self.frameSize().height()
        self.MotWidget = QtWidgets.QWidget(self)
        self.MotWidget.setGeometry(QtCore.QRect(1/4*self.width, 1/3*self.height, 350, 130))
        self.MotWidget.setStyleSheet("""
                                     .QWidget {
                                     border: 10px solid black;
                                     border-radius: 10px;
                                     background-color: rgb(255, 255, 255);
                                     }
                                     """)
        self.MotWidget.setObjectName("MotWidget")
        #formLayout pour afficher le mot et la traduction
        self.formLayoutMot = QtWidgets.QFormLayout(self.MotWidget)
        self.formLayoutMot.setContentsMargins(40, 30, 30, 30)
        self.formLayoutMot.setObjectName("formLayoutMot")
        #deux labels de traduction
        self.labMot = QtWidgets.QLabel(u"Mot:", self.MotWidget)
        self.labMot.setObjectName("labMot")
        self.labMot.setAlignment(QtCore.Qt.AlignRight)
        self.labMot.setFont(QFont("Roman times", 8, QFont.Bold))
        self.formLayoutMot.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labMot)
        self.labMotAns = QtWidgets.QLabel(self.MotWidget)
        self.labMotAns.setObjectName("labMotAns")
        self.labMotAns.setAlignment(QtCore.Qt.AlignVCenter)
        self.labMotAns.setFont(QFont("Arial", 8, QFont.Bold))
        self.formLayoutMot.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labMotAns)
        #deux labels de Traduction
        self.labTra = QtWidgets.QLabel(u"Traduction:", self.MotWidget)
        self.labTra.setObjectName("labTra")
        self.labTra.setAlignment(QtCore.Qt.AlignRight)
        self.labTra.setFont(QFont("Roman times", 8, QFont.Bold))
        self.formLayoutMot.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labTra)
        self.labTraAns = QtWidgets.QLabel("", self.MotWidget)
        self.labTraAns.setObjectName("labTraAns")
        self.labTraAns.setAlignment(QtCore.Qt.AlignVCenter)
        self.labTraAns.setFont(QFont("Arial", 8, QFont.Bold))
        self.formLayoutMot.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labTraAns)
        self.sujet = getTradRandom(self.cartesJouees[0], self.cartesJouables)
        self.labMotAns.setText(self.sujet[0])
        self.labTraAns.setText(self.sujet[1])
        self.cardIndex = 0
        #Label "Est-ce que..."
        self.lab1 = QtWidgets.QLabel(u"Q {}/{}: La traduction du mot est-elle correcte?".format(self.cardIndex+1, len(self.cartesJouees)), self)
        self.lab1.setAlignment(QtCore.Qt.AlignCenter)
        self.lab1.setGeometry(QtCore.QRect(1/4*self.width-35, 1/3*self.height-40, 418, 19))
        self.lab1.setFont(QFont("Roman times", 8, QFont.Bold))
        self.lab1.setObjectName("lab1")
        self.vraiFauxWidget = QtWidgets.QWidget(self)
        self.vraiFauxWidget.setGeometry(QtCore.QRect(1/3*self.width-40, 2/3*self.height-20, 321, 71))
        self.vraiFauxWidget.setObjectName("vraiFauxWidget")
        #horizontalLayout pour les boutons vrai et faux
        self.horLayoutVraiFaux = QtWidgets.QHBoxLayout(self.vraiFauxWidget)
        self.horLayoutVraiFaux.setContentsMargins(0, 0, 0, 0)
        self.horLayoutVraiFaux.setObjectName("horLayoutVraiFaux")
        #bouton Vrai
        self.btnVrai = QtWidgets.QPushButton(u"Vrai", self.vraiFauxWidget)
        self.btnVrai.setFont(QFont("Roman times", 8, QFont.Bold))
        self.btnVrai.setObjectName("btnVrai")
        self.btnVrai.clicked.connect(self.click_vrai)
        self.horLayoutVraiFaux.addWidget(self.btnVrai)
        #spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horLayoutVraiFaux.addItem(spacerItem)
        #bouton faux
        self.btnFaux = QtWidgets.QPushButton(u"Faux", self.vraiFauxWidget)
        self.btnFaux.setFont(QFont("Roman times", 8, QFont.Bold))
        self.btnFaux.setObjectName("btnFaux")
        self.btnFaux.clicked.connect(self.click_faux)
        self.horLayoutVraiFaux.addWidget(self.btnFaux)
        
        #le message de victoire
        self.victoryWidget=QWidget(self)
        self.victoryWidget.resize(300, 200)
        qr=self.victoryWidget.frameGeometry()
        qr.moveCenter(self.rect().center())
        self.victoryWidget.move(qr.topLeft())
        self.label=QLabel(self.victoryWidget)
        path="view/icons/victory.png"
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
        path="view/icons/gameOver.png"
        self.pixmap=QtGui.QPixmap()
        self.pixmap.load(path)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True) 
        self.defeatWidget.setVisible(False)
        
    error=QtCore.pyqtSignal()
    success=QtCore.pyqtSignal()
    def click_vrai(self):
        if match(self.labMotAns.text(), self.labTraAns.text(), self.cartesJouables):
            self.success.emit()
        else:
            self.error.emit()
        if self.cardIndex == len(self.cartesJouees)-1:
            pass
        elif self.cardIndex < len(self.cartesJouees)-1:
            self.cardIndex += 1
            self.sujet = getTradRandom(self.cartesJouees[self.cardIndex], self.cartesJouables)
            self.labMotAns.setText(self.sujet[0])
            self.labTraAns.setText(self.sujet[1])
        self.lab1.setText(u"Q {}/{}: La traduction du mot est-elle correcte?".format(self.cardIndex+1, len(self.cartesJouees)))                    
    def click_faux(self):
        if not match(self.labMotAns.text(), self.labTraAns.text(), self.cartesJouables):
            self.success.emit()
        else:
            self.error.emit()
        if self.cardIndex == len(self.cartesJouees)-1:
            pass
        elif self.cardIndex < len(self.cartesJouees)-1:
            self.cardIndex += 1
            self.sujet = getTradRandom(self.cartesJouees[self.cardIndex], self.cartesJouables)
            self.labMotAns.setText(self.sujet[0])
            self.labTraAns.setText(self.sujet[1])
        self.lab1.setText(u"Q {}/{}: La traduction du mot est-elle correcte?".format(self.cardIndex+1, len(self.cartesJouees)))
        
        

class VraiFauxGame(QWidget):
    def __init__(self, givenWindow, cardsPlayed):
        super(vraiFauxGame, self).__init__(givenWindow)
        self.resize(givenWindow.frameSize())
        self.cartesJouables=cardsPlayed
        self.init()
    leave=QtCore.pyqtSignal()
    def init(self):
        self.cartesJouees=[]
        self.settingtime = AccessSettings.getGameSettings("rightwrong", 1)
        self.settingnb = AccessSettings.getGameSettings("rightwrong", 0)
        if self.settingnb <= len(self.cartesJouables):
            while (len(self.cartesJouees)<self.settingnb):
                i=randrange(0, len(self.cartesJouables))
                if (self.cartesJouables[i] not in self.cartesJouees):
                    self.cartesJouees.append(self.cartesJouables[i])
        else:
            self.cartesJouees = self.cartesJouables
        self.window=gameWindow.GameWindow(self, len(self.cartesJouees), self.settingtime)
        self.game=vraiFauxGameWindow(self.window.gameArea, self.cartesJouees, self.cartesJouables)
        self.cardNb = 0
        self.correctCardNb = 0
        self.window.show()
        
        self.window.resetSignal.connect(self.reset)
        self.window.leaveSignal.connect(self.endOfGame)
        self.game.error.connect(self.onError)
        self.game.success.connect(self.onSuccess)
        self.window.timeIsOut.connect(self.game.defeatWidget.show)
    def onError(self):
        self.cardNb += 1
        self.window.incrementErrorCount()
        if self.cardNb == len(self.cartesJouees):
            #QMessageBox.information(self,"Information", self.tr("    C'est la dernière carte!\nCliquez 'Reset' et réessayez!"))
            self.game.error.disconnect()
            self.game.success.disconnect()
    def onSuccess(self):
        self.cardNb += 1
        self.correctCardNb += 1
        self.window.incrementSuccessCount()
        if self.correctCardNb == len(self.cartesJouees):
            self.game.victoryWidget.show()
            self.game.error.disconnect()
            self.game.success.disconnect()
        elif self.correctCardNb != len(self.cartesJouees) and self.cardNb == len(self.cartesJouees):
            #QMessageBox.information(self,"Information", self.tr("    C'est la dernière carte!\nCliquez 'Reset' et réessayez!"))
            self.game.error.disconnect()
            self.game.success.disconnect()   
    def reset(self):
        self.game.close()
        #la ligne suivante evite que la fenetre, meme fermee, envoie le signal timeIsOut
        self.window.timeIsOut.disconnect()
        self.window.close()
        self.init()
    def endOfGame(self):
        self.leave.emit()
        self.close()



#if __name__ == "__main__":
#    Table='anglais'
#    ### cartes concernées par le jeu
#    CartesEnJeu=database.getCardsToLearn(Table,0,9)
#    args = sys.argv
#    b = QApplication(args)
#    w = QWidget()
#    #w.resize(853, 554)
#    w.resize(1000, 600)#on peut modifier
#    mf = vraiFauxGame(w, CartesEnJeu)
#    w.show()
#    b.exec_()
#    b.lastWindowClosed.connect(b.quit)

