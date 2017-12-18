from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys

from random import randrange

ListCartesEnJeu=["suspendre","remuer","amour","bonjour","douche","rideau","empreinte","carafe"]
ListTradsEnJeu=["sling","dwell","love","hello","shower","curtain","mark","carafe"]

class ButtonToDrag(QPushButton):
    def __init__(self, nom, place):
        super(ButtonToDrag, self).__init__(nom, place)
        self.setAcceptDrops(True)

    # event on veut bouger la carte
    def mouseMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(QtCore.Qt.MoveAction)
        print("moving...")

    # event on a bougé la carte sur une autre carte
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            print("dragging... ")
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            cardSource = event.source()
            print("droping...")
            # bouge les 2 cartes dans le coin en haut à gauche
            # dans tous les cas pour l'instant (juste ou nom)
            # il faut maintenant tester que trad !
            self.move(event.pos())
            cardSource.move(event.pos())
            event.accept()
        else:
            event.ignore()


class TestRelie(object):
    def __init__(self):
        ## la fenetre
        self.Dialog = QWidget()
        self.Dialog.setObjectName("Jeu de reliage")
        self.Dialog.setWindowTitle("Drag and Drop")
        self.Dialog.setFixedSize(633, 415)
        self.myCards=ListCartesEnJeu
        for i,carte in enumerate(ListCartesEnJeu) :
            self.myCards[i]=ButtonToDrag(carte, self.Dialog)
            myx=randrange(5,520,1)
            myy=randrange(5,380,1)
            self.myCards[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
        self.myTrads = ListTradsEnJeu
        for i, carte in enumerate(ListTradsEnJeu):
            self.myTrads[i] = ButtonToDrag(carte, self.Dialog)
            myx = randrange(5, 520, 1)
            myy = randrange(5, 380, 1)
            self.myTrads[i].setGeometry(QtCore.QRect(myx, myy, 113, 32))
            self.myTrads[i].setStyleSheet("background-color: rgb(122, 227, 255);\n" "border-color: rgb(0, 0, 0);\n" "font: 75 13pt \"Helvetica Neue\";")

    #### il faut bouger un bouton sur un autre
    #### la classe ButtonToDrag gere les events

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def close(self):
        self.Dialog.close()


if __name__ == "__main__":
    args = sys.argv
    b = QApplication(args)
    mf = TestRelie()
    mf.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)
