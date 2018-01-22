############# definition de l'interface de creation de flash cards

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, \
    QProgressBar, QSlider, QComboBox, QFileDialog, QFrame

import sys

from controller import AccessSettings

class mySettings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        ## la fenetre
        self.setObjectName("Current Settings")
        self.setFixedSize(497, 492)
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
        self.langue.setText(" Le language par défault :")
        self.editlangue = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.editlangue, 1, 1, 1, 3)
        self.editlangue.setText(currentSettings[0])

        # ligne 2 : user par défaut
        self.user = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.user, 2, 0, 1, 3)
        self.user.setText(" L'utilisateur en cours est : ")
        self.edituser = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.edituser, 2, 1, 1, 3)
        self.edituser.setText(currentSettings[1])

        # tableau 2x5 sur un bloc 3x6 pour les parametre des jeux
        # les caractéristiques
        self.nbcards = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.nbcards, 4, 0, 1, 1)
        self.nbcards.setText("Nombre de cartes à jouer ")
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

        ## le layout du haut
        self.whatWidget = QWidget(self)
        self.whatWidget.setGeometry(QtCore.QRect(10, 10, 451, 31))
        self.whatWidget.setObjectName("whatWidget")
        self.togivename = QHBoxLayout(self.whatWidget)
        self.togivename.setContentsMargins(0, 0, 0, 0)
        self.togivename.setObjectName("togivename")
        self.explain = QLabel(self.whatWidget)
        self.explain.setObjectName("explain")
        self.explain.setText(" Vous pouvez mettre à jous les paramètres de l'application ci-dessous :")
        self.togivename.addWidget(self.explain)

        ## le layout du bas
        self.bottomWidget = QWidget(self)
        self.bottomWidget.setGeometry(QtCore.QRect(10, 400, 451, 32))
        self.bottomWidget.setObjectName("bottomWidget")
        self.toUpdate = QHBoxLayout(self.bottomWidget)
        self.toUpdate.setContentsMargins(0, 0, 0, 0)
        self.toUpdate.setObjectName("toUpdate")
        # bouton de mise a jour
        self.updateButton = QPushButton(u"Update", self.bottomWidget)
        self.updateButton.setObjectName("updateButton")
        self.updateButton.addWidget(self.updateButton)

        ## gestion des slots et signaux
        self.updateButton.clicked.connect(self.update)

    updatedSettings =QtCore.pyqtSignal()

    def update(self):
        allGameNames = AccessSettings.getAllGameNames()
        self.close()
