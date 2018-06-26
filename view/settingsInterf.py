############# definition de l'interface de creation de flash cards
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout

import sys

from view import AccessSettings

class mySettings(QWidget):
    def __init__(self, parent, previousDisplay):
        self.nextDisplay = previousDisplay
        self.parentWindow=parent
    def stealTheLimelight(self):
        super().__init__(self.parentWindow)
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
        
        # ligne 3 : pixabay API key
        self.key = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.key, 3, 0, 1, 3)
        self.key.setText("Utilisateur en cours : ")
        self.editkey = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.editkey, 3, 2, 1, 2)
        self.editkey.setText(currentSettings[2])

        # tableau 2x5 sur un bloc 3x6 pour les parametre des jeux
        # pour la forme
        self.notvisible = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.notvisible, 4, 0, 1, 1)
        #self.notvisible.setVisible(False)
        # les caractéristiques
        self.nbcards = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.nbcards,5, 0, 1, 1)
        self.nbcards.setText("Nombre de cartes")
        self.chrono = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.chrono, 6, 0, 1, 1)
        self.chrono.setText("Temps de jeu")
        # les jeux
        allGameNames = AccessSettings.getAllGameNames()
        self.gamelabel= allGameNames.copy()
        self.nbcardsEdit = allGameNames.copy()
        self.chronoEdit = allGameNames.copy()
        for rank,GameName in enumerate(allGameNames):
            self.gamelabel[rank] = QLabel(self.gridWidget)
            self.answergrid.addWidget(self.gamelabel[rank], 4, rank+1, 1, 1)
            self.gamelabel[rank].setText(GameName)
            self.nbcardsEdit[rank] = QLineEdit(self.gridWidget)
            self.answergrid.addWidget(self.nbcardsEdit[rank], 5, rank+1, 1, 1)
            self.nbcardsEdit[rank].setText(currentSettings[3][rank])
            self.chronoEdit[rank] = QLineEdit(self.gridWidget)
            self.answergrid.addWidget(self.chronoEdit[rank], 6, rank+1, 1, 1)
            self.chronoEdit[rank].setText(currentSettings[4][rank])

        ## le bouton du bas
        self.updateButton = QPushButton(u"Update", self.gridWidget)
        self.quitButton = QPushButton(u"Quit", self.gridWidget)
        self.answergrid.addWidget(self.updateButton, 7, 0, 1, 3)
        self.answergrid.addWidget(self.quitButton, 7, 3, 1, 3)

        ## gestion des slots et signaux
        self.updateButton.clicked.connect(self.update)
        self.quitButton.clicked.connect(self.redirect.emit)
        self.show()

    redirect = QtCore.pyqtSignal()

    def update(self):
        allGameNames = AccessSettings.getAllGameNames()
        # modification dans le xml de parametres
        AccessSettings.changeLangage(str(self.editlangue.text()))
        AccessSettings.changeUser(str(self.edituser.text()))
        AccessSettings.changeKey(str(self.editkey.text()))
        for rank, GameName in enumerate(allGameNames):
            AccessSettings.changeNbCards(str(self.nbcardsEdit[rank].text()),GameName)
            AccessSettings.changeChrono(str(self.chronoEdit[rank].text()), GameName)
        self.redirect.emit()

    def toTheShadows(self):
        self.close()
