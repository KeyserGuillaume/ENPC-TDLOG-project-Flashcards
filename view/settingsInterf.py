############# definition de l'interface de creation de flash cards

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout

import sys

from controller import AccessSettings

class mySettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        ## la fenetre
        self.setObjectName("Current Settings")
        self.setFixedSize(497, 492)

        ## le layout du haut
        self.whatWidget = QWidget(self)
        self.whatWidget.setGeometry(QtCore.QRect(10, 10, 451, 31))
        self.togivename = QHBoxLayout(self.whatWidget)
        self.togivename.setContentsMargins(0, 0, 0, 0)
        self.explain = QLabel(self.whatWidget)
        self.explain.setObjectName("explain")
        self.explain.setText(" Vous pouvez mettre à jous les paramètres de l'application ci-dessous :")
        self.togivename.addWidget(self.explain)

        ## le layout de la grille centrale
        self.gridWidget = QWidget(self)
        self.gridWidget.setGeometry(QtCore.QRect(10, 50, 451, 341))
        self.answergrid = QGridLayout(self.gridWidget)
        self.answergrid.setContentsMargins(0, 0, 0, 0)

        ## the current Settings
        currentSettings = AccessSettings.getAllSettings()

        # ligne 1 : langue par défaut
        self.langue = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.langue, 1, 0, 1, 3)
        self.langue.setText("Language par défault :")
        self.editlangue = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.editlangue, 1, 2, 1, 2)
        self.editlangue.setText(currentSettings[0])

        # ligne 2 : user par défaut
        self.user = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.user, 2, 0, 1, 3)
        self.user.setText("Utilisateur en cours : ")
        self.edituser = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.edituser, 2, 2, 1, 2)
        self.edituser.setText(currentSettings[1])

        # tableau 2x5 sur un bloc 3x6 pour les parametre des jeux
        # pour la forme
        self.notvisible = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.notvisible, 3, 0, 1, 1)
        #self.notvisible.setVisible(False)
        # les caractéristiques
        self.nbcards = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.nbcards, 4, 0, 1, 1)
        self.nbcards.setText("Nombre de cartes")
        self.chrono = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.chrono, 5, 0, 1, 1)
        self.chrono.setText("Temps de jeu")
        # les jeux
        allGameNames = AccessSettings.getAllGameNames()
        self.gamelabel= allGameNames.copy()
        self.nbcardsEdit = allGameNames.copy()
        self.chronoEdit = allGameNames.copy()
        for rank,GameName in enumerate(allGameNames):
            self.gamelabel[rank] = QLabel(self.gridWidget)
            self.answergrid.addWidget(self.gamelabel[rank], 3, rank+1, 1, 1)
            self.gamelabel[rank].setText(GameName)
            self.nbcardsEdit[rank] = QLineEdit(self.gridWidget)
            self.answergrid.addWidget(self.nbcardsEdit[rank], 4, rank+1, 1, 1)
            self.nbcardsEdit[rank].setText(currentSettings[2][rank])
            self.chronoEdit[rank] = QLineEdit(self.gridWidget)
            self.answergrid.addWidget(self.chronoEdit[rank], 5, rank+1, 1, 1)
            self.chronoEdit[rank].setText(currentSettings[3][rank])

        ## le bouton du bas
        self.updateButton = QPushButton(u"Update", self.gridWidget)
        self.quitButton = QPushButton(u"Quit", self.gridWidget)
        self.answergrid.addWidget(self.updateButton, 6, 0, 1, 3)
        self.answergrid.addWidget(self.quitButton, 6, 3, 1, 3)

        ## gestion des slots et signaux
        self.updateButton.clicked.connect(self.update)
        self.quitButton.clicked.connect(self.quit)

    updated = QtCore.pyqtSignal()

    def update(self):
        allGameNames = AccessSettings.getAllGameNames()
        # modification dans le xml de parametres
        AccessSettings.changeLangage(str(self.editlangue.text()))
        AccessSettings.changeUser(str(self.edituser.text()))
        for rank, GameName in enumerate(allGameNames):
            AccessSettings.changeNbCards(str(self.nbcardsEdit[rank].text()),GameName)
            AccessSettings.changeChrono(str(self.chronoEdit[rank].text()), GameName)
        self.updated.emit()
        self.close()

    def quit(self):
        self.updated.emit()
        self.close()

'''
if __name__ == "__main__":
    args = sys.argv
    a = QApplication(args)
    w = QWidget()
    w.resize(497, 492)
    mf = mySettings(w)
    mf.updated.connect(w.close)
    w.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)
'''
