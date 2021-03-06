# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLCDNumber, QLabel
import sys
from model import database
from view.games import gameWindow
from controller import AccessSettings
import random
from random import randint

#### match (meme carte) entre mot et trad dans cet ordre
def match(text1,text2):
    answer=False
    matching=database.getCompleteCardsWithAttribute('anglais', 'mot', text1)
    for card in matching:
        answer = answer or (text2==card.trad)
    return answer

def getMotTradRandom(CardsPlayed):
    result = []
    i=random.randint(1,3)
    if i == 1:
        j = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[j].word)
        result.append(CardsPlayed[j].trad)
        k = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[k].trad)
        l = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[l].trad)   
    elif i == 2:
        j = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[j].word)
        k = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[k].trad)
        result.append(CardsPlayed[j].trad)
        l = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[l].trad)
    elif i == 3:
        j = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[j].word)
        k = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[k].trad)
        l = random.randint(0, len(CardsPlayed)-1)
        result.append(CardsPlayed[l].trad) 
        result.append(CardsPlayed[j].trad)
    return result  



class pointToCardGameWindow(QWidget):
    def __init__(self,bigWindow, CardsPlayed):
        ## la fenetre de jeux
        super(pointToCardGameWindow, self).__init__(bigWindow)
        self.cartesJouees=CardsPlayed
        self.setWindowTitle("Point To Card")
        self.resize(bigWindow.frameSize())
        self.width=self.frameSize().width()
        self.height=self.frameSize().height()
        self.MotWidget = QtWidgets.QWidget(self)
        self.MotWidget.setGeometry(QtCore.QRect(1/3*self.width+40, 1/3*self.height, 581, 61))
        #formLayout pour afficher le mot et la traduction
        self.formLayoutMot = QtWidgets.QFormLayout(self.MotWidget)
        self.formLayoutMot.setContentsMargins(0, 0, 0, 0)
        #deux labels de traduction
        self.labMot = QtWidgets.QLabel(u"Mot:", self.MotWidget)
        self.formLayoutMot.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labMot)
        self.labMotAns = QtWidgets.QLabel(self.MotWidget)
        self.formLayoutMot.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labMotAns)
        #deux labels de Traduction
        #self.labTra = QtWidgets.QLabel(u"Traduction:", self.MotWidget)
        #self.formLayoutMot.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labTra)
        #self.labTraAns = QtWidgets.QLabel("", self.MotWidget)
        #self.formLayoutMot.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labTraAns)
        sujet = getMotTradRandom(self.cartesJouees)
        self.labMotAns.setText(sujet[0])
        #self.labTraAns.setText(sujet[1])
        #Label "Est-ce que..."
        self.lab1 = QtWidgets.QLabel(u"Choisir la bonne traduction", self)
        self.lab1.setGeometry(QtCore.QRect(1/4*self.width+20, 1/3*self.height-40, 418, 19))
        self.lab1.setFont(QFont("Roman times", 8, QFont.Bold))
        self.choiceWidget = QtWidgets.QWidget(self)
        self.choiceWidget.setGeometry(QtCore.QRect(1/3*self.width-40, 1/2*self.height, 321, 71))
        #horizontalLayout pour les boutons vrai et faux
        self.horLayoutVraiFaux = QtWidgets.QHBoxLayout(self.choiceWidget)
        self.horLayoutVraiFaux.setContentsMargins(0, 0, 0, 0)
        #bouton 1
        self.btn1 = QtWidgets.QPushButton(sujet[1], self.choiceWidget)
        self.btn1.clicked.connect(self.click_checkbtn1)
        self.horLayoutVraiFaux.addWidget(self.btn1)
        #bouton 1
        self.btn2 = QtWidgets.QPushButton(sujet[2], self.choiceWidget)
        self.btn2.clicked.connect(self.click_checkbtn2)
        self.horLayoutVraiFaux.addWidget(self.btn2)
        #bouton 1
        self.btn3 = QtWidgets.QPushButton(sujet[3], self.choiceWidget)
        self.btn3.clicked.connect(self.click_checkbtn3)
        self.horLayoutVraiFaux.addWidget(self.btn3)
        #spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horLayoutVraiFaux.addItem(spacerItem)
        #bouton faux
        #self.btnFaux = QtWidgets.QPushButton(u"Faux", self.choiceWidget)
        #self.btnFaux.clicked.connect(self.click_faux)
        #self.horLayoutVraiFaux.addWidget(self.btnFaux)
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
    def click_checkbtn1(self):
        if match(self.labMotAns.text(), self.btn1.text()):
            self.success.emit()
        else:
            self.error.emit()
        newsujet = getMotTradRandom(self.cartesJouees)
        print(newsujet)
        self.labMotAns.setText(newsujet[0])
        self.btn1.setText(newsujet[1])
        self.btn2.setText(newsujet[2])
        self.btn3.setText(newsujet[3])

    def click_checkbtn2(self):
        if match(self.labMotAns.text(), self.btn2.text()):
            self.success.emit()
        else:
            self.error.emit()
        newsujet = getMotTradRandom(self.cartesJouees)
        print(newsujet)
        self.labMotAns.setText(newsujet[0])
        self.btn1.setText(newsujet[1])
        self.btn2.setText(newsujet[2])
        self.btn3.setText(newsujet[3])

    def click_checkbtn3(self):
        if match(self.labMotAns.text(), self.btn3.text()):
            self.success.emit()
        else:
            self.error.emit()
        newsujet = getMotTradRandom(self.cartesJouees)
        print(newsujet)
        self.labMotAns.setText(newsujet[0])
        self.btn1.setText(newsujet[1])
        self.btn2.setText(newsujet[2])
        self.btn3.setText(newsujet[3])

    

            
    '''def click_faux(self):
        if not match(self.labMotAns.text(), self.labTraAns.text()):
            self.success.emit()
        else:
            self.error.emit()
        sujet = getMotTradRandom(self.cartesJouees)
        self.labMotAns.setText(sujet[0])
        self.labTraAns.setText(sujet[1])     '''       
        
        

class pointToCardGame(QWidget):
    def __init__(self, givenWindow, cardsPlayed):
        super(pointToCardGame, self).__init__(givenWindow)
        self.resize(givenWindow.frameSize())
        self.cartesJouees=cardsPlayed
        self.init()
    leave=QtCore.pyqtSignal()
    def init(self):
        self.settingtime = AccessSettings.getGameSettings("pointto", 1)
        self.settingnb = AccessSettings.getGameSettings("pointto", 0)
        self.window=gameWindow.GameWindow(self, self.settingnb, self.settingtime)
        self.game=pointToCardGameWindow(self.window.gameArea, self.cartesJouees[0:self.settingnb])
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
        self.game.lab1.setText("")
        self.game.labMot.setText("")
        self.game.labMotAns.setText(u"TIME IS OUT")
        #self.game.labTra.setText("")
        #self.game.labTraAns.setText(u"GAME OVER")
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
    w.resize(1000, 600)#on peut modifier
    mf = pointToCardGame(w, CartesEnJeu)
    w.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
'''