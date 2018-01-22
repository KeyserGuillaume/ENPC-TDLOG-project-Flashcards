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
        self.answergrid.addWidget(self.langue, 1, 0, 1, 1)
        self.langue.setText(" Le language par défault :")
        self.editlangue = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.editlangue, 1, 1, 1, 1)
        self.editlangue.setText(currentSettings[0])

        # ligne 2 : user par défaut
        self.user = QLabel(self.gridWidget)
        self.answergrid.addWidget(self.user, 2, 0, 1, 1)
        self.user.setText(" L'utilisateur en cours est : ")
        self.edituser = QLineEdit(self.gridWidget)
        self.answergrid.addWidget(self.edituser, 2, 1, 1, 1)
        self.edituser.setText(currentSettings[1])

        # ligne 3 à 12
        # insérer un tableau

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
        self.updateButton.clicked.connect(self.commit)

    updatedSettings =QtCore.pyqtSignal()

    def languageChosen(self):
        langue = str(self.editlanguage.currentText())
        if (langue == "Other"):
            self.setLanguage.setEnabled(True)
            return
        self.setname.setText(str(database.giveNewCardName(langue)))

    def newLanguage(self):
        self.setname.setText("1")


#renamed it because it's used both for creating and modifying
    def commit(self):
        name = str(self.setname.text())
        mot = str(self.editword.text())
        traduction = str(self.edittrad.text())
        phrase = str(self.editexample.text())
        theme = str(self.editthema.text())
        difficulte = str(round(self.editdifficult.value() / 10))
        maitrise = str(round(self.editproficiency.value() / 10))
        illustrationpath = self.image
        soundpath = self.sound
        nature = str(self.editnature.currentText())
        langue = str(self.editlanguage.currentText())
        if mot=="":
            self.myword.setText(" Entrez votre mot : (Non facultatif !)")
            return
        if traduction=="":
            self.mytrad.setText(" Entrez sa traduction : (Non facultatif !)")
            return
        if langue == "Other":
            langue = str(self.setLanguage.text())
            if (not (database.existsLanguage(langue))):
                database.addLanguage(langue)
        mycard = flashcard.FlashCards(str(database.giveNewCardName(langue)), mot, traduction, phrase, theme, difficulte,
                                      maitrise, illustrationpath, soundpath, nature, langue)
        if database.getNextId(langue) <= int(name):
            database.register(mycard)
            self.created.emit()
        else:  # nom deja existant dans la table
            database.modifyCard(langue, name, traduction, phrase, theme, difficulte, maitrise, illustrationpath,
                                soundpath, nature)
            self.modified.emit()
        if (not database.existeSameCard(langue, mot, traduction)):
            database.register(mycard)
        else:
            #l'utilisateur a entre une carte pour un mot deja entre
            #il faudrait lui demander s'il souhaite ecrire par dessus 
            #la carte deja existante, en lui affichant cette carte si possible
            self.close()
        self.close()
        ## inserer un appel a la fonction permettant de sauvegarder les cartes crees ici
        # return mycard
