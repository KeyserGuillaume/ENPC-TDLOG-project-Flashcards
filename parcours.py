from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
import sys
import database

import DragDrop

from icons import icons
# permet l'accès aux images des icones

AllLangages = database.giveAllLanguages()

_root = QtCore.QFileInfo(__file__).absolutePath()

class parcoursLanguesFolder(object):
    def __init__(self, Dialog):
        Dialog.resize(685, 430)
        self.gridWidget = QWidget(Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setObjectName("grille de placement")
        self.folderGrid = QGridLayout(self.gridWidget)
        self.folderGrid.setContentsMargins(0, 0, 0, 0)
        self.folderGrid.setObjectName("folderGrid")
        self.myfolders = AllLangages
        for i, langue in enumerate(AllLangages):
            self.myfolders[i] = QPushButton(langue, self.gridWidget)
            self.myfolders[i].setMinimumSize(QtCore.QSize(101, 91))
            self.myfolders[i].setMaximumSize(QtCore.QSize(101, 91))
            self.myfolders[i].setStyleSheet("background-image: url(:/icons/dossier.png);\n" "font: 75 14pt \"Arial\";")
            self.myfolders[i].setObjectName(langue)
            row = i/4
            column = i%4
            self.folderGrid.addWidget(self.myfolders[i], row, column, 1, 1)


class parcoursIconsGame(object):
    def __init__(self, Dialog):
        Dialog.resize(663, 406)
        self.gridWidget = QWidget(Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridWidget.setObjectName("gridWidget")
        self.gameGrid = QGridLayout(self.gridWidget)
        self.gameGrid.setContentsMargins(0, 0, 0, 0)
        self.gameGrid.setObjectName("gameGrid")
        # drag and drop game
        self.DDButton = QPushButton(u" ", self.gridWidget)
        self.DDButton.setMinimumSize(QtCore.QSize(101, 101))
        self.DDButton.setMaximumSize(QtCore.QSize(101, 101))
        self.DDButton.setStyleSheet("background-image: url(:/icons/dragdrop.png);")
        self.DDButton.setObjectName("DDButton")
        self.gameGrid.addWidget(self.DDButton, 0, 0, 1, 1)
        # memory game
        self.MemoryButton = QPushButton(u" ", self.gridWidget)
        self.MemoryButton.setMinimumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setMaximumSize(QtCore.QSize(101, 101))
        self.MemoryButton.setStyleSheet("background-image: url(:/icons/memory.png);")
        self.MemoryButton.setObjectName("MemoryButton")
        self.gameGrid.addWidget(self.MemoryButton, 0, 1, 1, 1)
        # hot or cold game
        self.HCButton = QPushButton(u" ", self.gridWidget)
        self.HCButton.setMinimumSize(QtCore.QSize(101, 101))
        self.HCButton.setMaximumSize(QtCore.QSize(101, 101))
        self.HCButton.setStyleSheet("background-image: url(:/icons/hotcold.png);")
        self.HCButton.setObjectName("HCButton")
        self.gameGrid.addWidget(self.HCButton, 0, 2, 1, 1)
        # point the answer game
        self.pointButton = QPushButton(u" ", self.gridWidget)
        self.pointButton.setMinimumSize(QtCore.QSize(131, 101))
        self.pointButton.setMaximumSize(QtCore.QSize(131, 101))
        self.pointButton.setStyleSheet("background-image: url(:/icons/pointTo.png);")
        self.pointButton.setObjectName("pointButton")
        self.gameGrid.addWidget(self.pointButton, 0, 3, 1, 1)

        ## signaux et slots : ouverture de la fenetre de jeux
        self.DDInterf = None
        self.DDButton.clicked.connect(self.openDD)

    def openDD(self):
        # ouverture de l'interface de jeu
        self.DDInterf = DragDrop.GameWindow()
        self.DDInterf.show()

def main():
    args = sys.argv
    a = QApplication(args)
    MyDialog=QWidget()
    mf = parcoursIconsGame(MyDialog)
    #mf.setupUi(MyDialog)
    MyDialog.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
