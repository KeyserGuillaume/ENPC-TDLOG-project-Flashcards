############# definition de l'interface de creation de flasch cards

## reste a gerer les boutons choisir
## il faut aussi ameliorer la gestion de la progression
## comment imporeter graphiquement une adresse de fichier ?
## inserer un appel a la fonction permettant de sauvegarder les cartes crees  --> ecriture dans un fichier ?

import flashcard

## a aller récupérer dans une base de donnée plus tard
langues=["anglais", "other"]
natureGram=["noun", "adjective", "verbe", "adverbe", "preposition", "exclamation",  "other"]

import sys
from PyQt5 import QtCore, QtWidgets  #, QtGui

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox

class CardCreation(object):
    def __init__(self):
        ## la fenetre
        self.Dialog=QWidget()
        self.Dialog.setObjectName("Card Creation")
        self.Dialog.setFixedSize(497, 492)
        ## le layout de la grille centrale
        self.answergridWidget = QWidget(self.Dialog)
        self.answergridWidget.setGeometry(QtCore.QRect(10, 50, 451, 341))
        self.answergridWidget.setObjectName("answergridWidget")
        self.answergrid = QGridLayout(self.answergridWidget)
        self.answergrid.setContentsMargins(0, 0, 0, 0)
        self.answergrid.setObjectName("answergrid")
        # remplissage avec infos et lignes de réponse
        # sous la forme un QLabel et un QLineEdit par ligne
        # sauf pour les images/sons a importer ou on met un QPushButton
        # et pour la maitrise / difficulte avec un curseur
        # ligne 1 : entrer le mot
        self.myword = QLabel(self.answergridWidget)
        self.myword.setObjectName("myword")
        self.answergrid.addWidget(self.myword, 1, 0, 1, 1)
        self.myword.setText(" Entrez votre mot :")
        self.editword = QLineEdit(self.answergridWidget)
        self.editword.setObjectName("editword")
        self.answergrid.addWidget(self.editword, 1, 1, 1, 1)
        # ligne 2 : entrer la traduction
        self.mytrad = QLabel(self.answergridWidget)
        self.mytrad.setObjectName("mytrad")
        self.answergrid.addWidget(self.mytrad, 2, 0, 1, 1)
        self.mytrad.setText(" Entrez sa traduction : ")
        self.edittrad = QLineEdit(self.answergridWidget)
        self.edittrad.setObjectName("edittrad")
        self.answergrid.addWidget(self.edittrad, 2, 1, 1, 1)
        # ligne 3 : entrer le theme
        self.mythema = QLabel(self.answergridWidget)
        self.mythema.setObjectName("mythema")
        self.answergrid.addWidget(self.mythema, 3, 0, 1, 1)
        self.mythema.setText(" Entrez le thème : ")
        self.editthema = QLineEdit(self.answergridWidget)
        self.editthema.setObjectName("editthema")
        self.answergrid.addWidget(self.editthema, 3, 1, 1, 1)
        # ligne 5 : entrer un exemple
        self.myexample = QLabel(self.answergridWidget)
        self.myexample.setObjectName("myexample")
        self.answergrid.addWidget(self.myexample, 5, 0, 1, 1)
        self.myexample.setText(" Entrez une phrase d\'exemple : ")
        self.editexample = QLineEdit(self.answergridWidget)
        self.editexample.setObjectName("editexample")
        self.answergrid.addWidget(self.editexample, 5, 1, 1, 1)
        # ligne 6 : entrer la difficulte
        self.dificult = QLabel(self.answergridWidget)
        self.dificult.setObjectName("dificult")
        self.answergrid.addWidget(self.dificult, 6, 0, 1, 1)
        self.dificult.setText(" Entrez la difficulté : ")
        #self.editdifficult = QLineEdit(self.answergridWidget)
        self.editdifficult = QSlider(self.answergridWidget)
        self.editdifficult.setOrientation(QtCore.Qt.Horizontal)
        self.editdifficult.setObjectName("editdifficult")
        self.answergrid.addWidget(self.editdifficult, 6, 1, 1, 1)
        # ligne 7 : entrer votre maitrise du mot
        self.myproficiency = QLabel(self.answergridWidget)
        self.myproficiency.setObjectName("myproficiency")
        self.answergrid.addWidget(self.myproficiency, 7, 0, 1, 1)
        self.myproficiency.setText(" Entrez votre niveau de maitrise :")
        #self.editproficiency = QLineEdit(self.answergridWidget)
        self.editproficiency = QSlider(self.answergridWidget)
        self.editproficiency.setOrientation(QtCore.Qt.Horizontal)
        self.editproficiency.setObjectName("editproficiency")
        self.answergrid.addWidget(self.editproficiency, 7, 1, 1, 1)
        # ligne 8 : indiquer la nature grammaticale du mot
        self.mynature = QLabel(self.answergridWidget)
        self.mynature.setObjectName("mynature")
        self.answergrid.addWidget(self.mynature, 8, 0, 1, 1)
        self.mynature.setText(" Selectionez la nature du mot :")
        self.editnature = QComboBox(self.answergridWidget)
        self.editnature.setObjectName("editnature")
        self.answergrid.addWidget(self.editnature, 8, 1, 1, 1)
        for naturespossibles in natureGram:
            self.editnature.addItem(naturespossibles)
        # ligne 9 : indiquer la langue
        self.mylanguage = QLabel(self.answergridWidget)
        self.mylanguage.setObjectName("mylanguage")
        self.answergrid.addWidget(self.mylanguage, 9, 0, 1, 1)
        self.mylanguage.setText(" Selectionez la langue :")
        self.editlanguage = QComboBox(self.answergridWidget)
        self.editlanguage.setObjectName("editlanguage")
        self.answergrid.addWidget(self.editlanguage, 9, 1, 1, 1)
        for languespossibles in langues:
            self.editlanguage.addItem(languespossibles)
        # ligne 10 : charge une image
        self.myillustration = QLabel(self.answergridWidget)
        self.myillustration.setObjectName("myillustration")
        self.answergrid.addWidget(self.myillustration, 10, 0, 1, 1)
        self.myillustration.setText(" Selectionez une image :")
        self.chooseButton1 = QPushButton(u"Choisir", self.answergridWidget)
        self.chooseButton1.setObjectName("chooseButton1")
        self.answergrid.addWidget(self.chooseButton1, 10, 1, 1, 1)
        # ligne 11 : charger un fichier son de prononciation
        self.mysound = QLabel(self.answergridWidget)
        self.mysound.setObjectName("mysound")
        self.answergrid.addWidget(self.mysound, 11, 0, 1, 1)
        self.mysound.setText(" Selectionez une prononciation :")
        self.chooseButton2 = QPushButton(u"Choisir", self.answergridWidget)
        self.chooseButton2.setObjectName("chooseButton2")
        self.answergrid.addWidget(self.chooseButton2, 11, 1, 1, 1)

        ## le layout du haut
        self.nameWidget = QWidget(self.Dialog)
        self.nameWidget.setGeometry(QtCore.QRect(10, 10, 451, 31))
        self.nameWidget.setObjectName("nameWidget")
        self.togivename = QHBoxLayout(self.nameWidget)
        self.togivename.setContentsMargins(0, 0, 0, 0)
        self.togivename.setObjectName("togivename")
        # label et linedit pour entrer le nom de la carte
        self.mycardname = QLabel(self.nameWidget)
        self.mycardname.setObjectName("mycardname")
        self.mycardname.setText(" Entrez le nom de votre carte :")
        self.togivename.addWidget(self.mycardname)
        self.setname = QLineEdit(self.nameWidget)
        self.setname.setObjectName("setname")
        self.togivename.addWidget(self.setname)

        ## le layout du bas
        self.bottomWidget = QWidget(self.Dialog)
        self.bottomWidget.setGeometry(QtCore.QRect(10, 400, 451, 32))
        self.bottomWidget.setObjectName("bottomWidget")
        self.tocreate = QHBoxLayout(self.bottomWidget)
        self.tocreate.setContentsMargins(0, 0, 0, 0)
        self.tocreate.setObjectName("tocreate")
        # barre de progression indiquant a quel point la carte est complete
        self.progress=0 #niveau de progres de le remplissage de la carte
        self.progressBar = QProgressBar(self.bottomWidget)
        self.progressBar.setProperty("value", self.progress)
        self.progressBar.setObjectName("progressBar")
        self.tocreate.addWidget(self.progressBar)
        # bouton de creation
        self.createButton = QPushButton(u"Create", self.bottomWidget)
        self.createButton.setObjectName("createButton")
        self.tocreate.addWidget(self.createButton)

        ## gestion des slots et signaux
        # creation d'une carte
        self.createButton.clicked.connect(self.create)
        # mise a jour du progres
        self.setname.textEdited.connect(self.progression)
        #self.editword.textEdited.connect(self.progression)
        #self.edittrad.textEdited.connect(self.progression)
        #self.editexample.textEdited.connect(self.progression)
        #self.editthema.textEdited.connect(self.progression)
        self.editword.editingFinished.connect(self.progression)
        self.edittrad.editingFinished.connect(self.progression)
        self.editexample.editingFinished.connect(self.progression)
        self.editthema.editingFinished.connect(self.progression)
        #self.editdifficult.textEdited.connect(self.progression)
        #self.editproficiency.textEdited.connect(self.progression)
        
    def show(self):
        # ouvreture de la fenetre
        self.Dialog.show()
    def progression(self):
        self.progress+=15
        self.progress=min(self.progress,100)
        self.progressBar.setProperty("value", self.progress)
    def create(self):
        name=str(self.setname.text())
        mot=str(self.editword.text())
        traduction=str(self.edittrad.text())
        phrase=str(self.editexample.text())
        theme=str(self.editthema.text())
        difficulte= " "  #str(self.editdifficult.text())
        maitrise= " "  #str(self.editproficiency.text())
        illustrationpath=" "
        soundpath=" "
        nature=str(self.editnature.currentText())
        langue=str(self.editlanguage.currentText())
        mycard=flashcard.FlashCards(name, mot,traduction, phrase, theme, difficulte, maitrise, illustrationpath, soundpath, "noun", "anglais")
        mycard.register()
        ## inserer un appel a la fonction permettant de sauvegarder les cartes crees ici
        #return mycard
    def quit(self):
        exit(0)


if __name__ == "__main__":
    args=sys.argv
    a = QApplication(args)
    mf=CardCreation()
    mf.show()
    # appliquer les regles souhaitees
    resultat = a.exec_()
    #a.exec_()
    a.lastWindowClosed.connect(a.quit)
    #mf.quit()
    #sys.exit(resultat)

