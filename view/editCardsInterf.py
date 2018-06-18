from model import flashcard, database, soundAPI

## a aller récupérer dans une base de donnée plus tard
## toutes les langues prises en charges
langues = database.giveAllLanguages()  # ["anglais", "other"]
# les classes grammaticales dispo (definitif)
natureGram = ["noun", "adjective", "verbe", "adverbe", "pronoun", "preposition",\
 "conjunction", "interjection", "determiner", "other"]

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit,\
 QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox,\
 QFileDialog, QFrame

import sys

class pop_upWidget(QWidget):
    def __init__(self, parent, queryText, yesText, noText):
        super().__init__(parent)
        self.resize(451, 80)
        self.gridLayout=QGridLayout(self)
        self.query=QLabel(queryText, self)
        self.gridLayout.addWidget(self.query, 0, 0, 1, 2)
        self.yesButton=QPushButton(yesText, self)
        self.gridLayout.addWidget(self.yesButton, 1, 0, 1, 1)
        self.noButton=QPushButton(noText, self)
        self.gridLayout.addWidget(self.noButton, 1, 1, 1, 1)        
        
        #signals and slots
        self.yesButton.clicked.connect(self.choice1)
        self.noButton.clicked.connect(self.choice2)
    accept=QtCore.pyqtSignal()
    refuse=QtCore.pyqtSignal()
    def choice1(self):
        self.accept.emit()
        self.close()
    def choice2(self):
        self.refuse.emit()
        self.close()

class SearchDirectory(QWidget):
    def __init__(self):
        super().__init__()
        self._myname = ""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Select your file",
                                                  "",
                                                  "Image Files (*.png *.jpg *.jp2 *.bmp *.tiff *.xpm *.gif *.webp *.eps);;Sound Files (*.mp3 *.wav *.m4a *.aac *.aiff *.gsm *.m4p *.wma);;All Files (*)",
                                                  options=options)
        if fileName:
            self._myname = fileName

    @property
    def name(self):
        return self._myname


class CardCreation(QWidget):
    def __init__(self, parent, previousDisplay, language):
        self.parent = parent
        self.nextDisplay = previousDisplay
        self.language = language
    def stealTheLimelight(self):
        super().__init__(self.parent)
        ## la fenetre
        self.setFixedSize(497, 492)
        ## le layout de la grille centrale
        self.answergridWidget = QWidget(self)
        self.answergridWidget.setGeometry(QtCore.QRect(10, 50, 451, 341))
        self.answergrid = QGridLayout(self.answergridWidget)
        self.answergrid.setContentsMargins(0, 0, 0, 0)
        # remplissage avec infos et lignes de réponse
        # sous la forme un QLabel et un QLineEdit par ligne
        # sauf pour les images/sons a importer ou on met un QPushButton
        # et pour la maitrise / difficulte avec un curseur
        # ligne 1 : entrer le mot
        self.myword = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.myword, 1, 0, 1, 1)
        self.myword.setText(" Entrez votre mot :")
        self.editword = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.editword, 1, 1, 1, 1)
        # ligne 2 : entrer la traduction
        self.mytrad = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mytrad, 2, 0, 1, 1)
        self.mytrad.setText(" Entrez sa traduction : ")
        self.edittrad = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.edittrad, 2, 1, 1, 1)
        # ligne 3 : entrer le theme
        self.mythema = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mythema, 3, 0, 1, 1)
        self.mythema.setText(" Entrez le thème : ")
        self.editthema = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.editthema, 3, 1, 1, 1)
        # ligne 5 : entrer un exemple
        self.myexample = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.myexample, 5, 0, 1, 1)
        self.myexample.setText(" Entrez une phrase d\'exemple : ")
        self.editexample = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.editexample, 5, 1, 1, 1)
        # ligne 6 : entrer la difficulte
        self.dificult = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.dificult, 6, 0, 1, 1)
        self.dificult.setText(" Entrez la difficulté : ")
        # self.editdifficult = QLineEdit(self.answergridWidget)
        self.editdifficult = QSlider(self.answergridWidget)
        self.editdifficult.setOrientation(QtCore.Qt.Horizontal)
        self.answergrid.addWidget(self.editdifficult, 6, 1, 1, 1)
        # ligne 7 : entrer votre maitrise du mot
        self.myproficiency = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.myproficiency, 7, 0, 1, 1)
        self.myproficiency.setText(" Entrez votre niveau de maitrise :")
        # self.editproficiency = QLineEdit(self.answergridWidget)
        self.editproficiency = QSlider(self.answergridWidget)
        self.editproficiency.setOrientation(QtCore.Qt.Horizontal)
        self.answergrid.addWidget(self.editproficiency, 7, 1, 1, 1)
        # ligne 8 : indiquer la nature grammaticale du mot
        self.mynature = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mynature, 8, 0, 1, 1)
        self.mynature.setText(" Sélectionnez la nature du mot :")
        self.editnature = QComboBox(self.answergridWidget)
        self.answergrid.addWidget(self.editnature, 8, 1, 1, 1)
        for naturespossibles in natureGram:
            self.editnature.addItem(naturespossibles)
        # ligne 9 : indiquer la langue
        self.mylanguage = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mylanguage, 9, 0, 1, 1)
        self.mylanguage.setText(" Sélectionnez la langue :")
        self.editlanguage = QComboBox(self.answergridWidget)
        self.answergrid.addWidget(self.editlanguage, 9, 1, 1, 1)
        for languespossibles in langues:
            self.editlanguage.addItem(languespossibles)
        self.editlanguage.addItem("Other")
        # ligne 10 : entrer une nouvelle langue
        self.myLanguage = QLabel(self.answergridWidget)
        self.myLanguage.setText(" Définissez la nouvelle langue :")
        self.myLanguage.setVisible(False)
        self.answergrid.addWidget(self.myLanguage, 10, 0, 1, 1)
        self.setLanguage = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.setLanguage, 10, 1, 1, 1)
        self.setLanguage.setEnabled(False)
        # ligne 11 : charge une image
        self.myillustration = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.myillustration, 11, 0, 1, 1)
        self.myillustration.setText(" Sélectionnez une image :")
        self.chooseButton1 = QPushButton(u"Choisir", self.answergridWidget)
        self.answergrid.addWidget(self.chooseButton1, 11, 1, 1, 1)
        self.image = ""
        # ligne 12 : charger un fichier son de prononciation
        self.recordButton = QPushButton("Record", self.answergridWidget)
        self.answergrid.addWidget(self.recordButton, 12, 0, 1, 1)
        self.listenButton = QPushButton("Listen", self.answergridWidget)
        self.listenButton.setEnabled(False)
        self.answergrid.addWidget(self.listenButton, 12, 1, 1, 1)
        self.frames=[]

        ## le layout du haut
        self.nameWidget = QWidget(self)
        self.nameWidget.setGeometry(QtCore.QRect(10, 10, 451, 31))
        self.togivename = QHBoxLayout(self.nameWidget)
        self.togivename.setContentsMargins(0, 0, 0, 0)
        # label et linedit pour entrer le nom de la carte
        self.mycardname = QLabel(self.nameWidget)
        self.mycardname.setText(" Le numéro de votre carte :")
        self.togivename.addWidget(self.mycardname)
        self.setname = QLineEdit(self.nameWidget)
        self.togivename.addWidget(self.setname)
        self.setname.setText(str(database.giveNewCardName('anglais')))
        self.setname.setEnabled(False)

        ## le layout du bas
        self.bottomWidget = QWidget(self)
        self.bottomWidget.setGeometry(QtCore.QRect(10, 400, 451, 32))
        self.tocreate = QHBoxLayout(self.bottomWidget)
        self.tocreate.setContentsMargins(0, 0, 0, 0)
        
        # bouton d'annulation
        self.cancelButton = QPushButton("Cancel", self.bottomWidget)
        self.tocreate.addWidget(self.cancelButton)        
        
        # bouton de creation
        self.createButton = QPushButton(u"Create", self.bottomWidget)
        self.tocreate.addWidget(self.createButton)
                
        self.setInitialLanguage(self.language)

        ## gestion des slots et signaux
        # fenetre de dialogue pour la selection d'un fichier
        self.chooseButton1.clicked.connect(self.browse1)
        self.recordButton.clicked.connect(self.record)
        self.listenButton.clicked.connect(self.listen)
        self.createButton.clicked.connect(self.commit)
        self.cancelButton.clicked.connect(self.redirect.emit)
        self.editlanguage.activated.connect(self.setCardIndex)
        self.setLanguage.editingFinished.connect(self.newLanguage)
        self.show()
    redirect=QtCore.pyqtSignal()

    def setCardIndex(self):
        langue = str(self.editlanguage.currentText())
        if (langue == "Other"):
            self.setLanguage.setEnabled(True)
            self.myLanguage.setVisible(True)
            return
        self.setname.setText(str(database.giveNewCardName(langue)))
    def setInitialLanguage(self, language):
        i=0
        while (self.editlanguage.currentText() != language and self.editlanguage.currentText() != "Other"):
            self.editlanguage.setCurrentIndex(i)
            i+=1
        self.setCardIndex()

    def newLanguage(self):
        self.setname.setText("1")

    def browse1(self):
        ex = SearchDirectory()
        self.image = ex.name

    def record(self):
        self.recordButton.setEnabled(False)
        self.listenButton.setEnabled(False)
        self.createButton.setEnabled(False)
        self.frames = soundAPI.recordSound()
        self.recordButton.setEnabled(True)
        self.listenButton.setEnabled(True)
        self.createButton.setEnabled(True)
    
    def listen(self):
        soundAPI.playSoundFromFrames(self.frames)
        
    def toTheShadows(self):
        self.close()

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
        if len(self.frames) > 0:
            soundpath = soundAPI.saveSound(langue, name, self.frames)
        else:
            soundpath = ""
        mycard = flashcard.FlashCards(str(database.giveNewCardName(langue)), 
                                      mot, traduction, phrase, theme, difficulte,
                                      maitrise, illustrationpath, soundpath, nature, langue)
        if database.getNextId(langue) <= int(name):
            database.register(mycard)
        else:  # nom deja existant dans la table
            database.modifyCard(langue, name, traduction, phrase, theme, 
                                difficulte, maitrise, illustrationpath,
                                soundpath, nature)
        if (not database.existsSameCard(langue, mot, traduction)):
            database.register(mycard)
        else:
            #l'utilisateur a entre une carte pour un mot deja entre
            #il faudrait lui demander s'il souhaite ecrire par dessus 
            #la carte deja existante, en lui affichant cette carte si possible
            self.close()
        self.redirect.emit()
        ## inserer un appel a la fonction permettant de sauvegarder les cartes crees ici

class CardModification(CardCreation):
    def __init__(self, parent, mycard, followUpDisplay):        
        super().__init__(parent, followUpDisplay, mycard.tablename)
        self.myCard = mycard
    def stealTheLimelight(self):
        super().stealTheLimelight()
        # remplissage avec les data existantes
        self.editword.setText(self.myCard.word)
        self.editword.setEnabled(False)
        self.edittrad.setText(self.myCard.trad)
        self.editexample.setText(self.myCard.exemple)
        self.editthema.setText(self.myCard.thema)
        self.editdifficult.setValue(self.myCard.howhard * 10)
        self.editproficiency.setValue(self.myCard.level * 10)
        #self.editlanguage.setCurrentText(self.myCard.tablename)
        self.editlanguage.setEnabled(False)
        self.editnature.setCurrentText(self.myCard.nature)
        self.setname.setText(str(self.myCard.name))
        self.createButton.setText("Modify")
        self.deleteWidget=QPushButton("delete", self.bottomWidget)
        self.tocreate.addWidget(self.deleteWidget)
        self.bottomWidget.resize(self.bottomWidget.sizeHint())
        self.deleteWidget.clicked.connect(self.confirmDeletion)
        cardFromDatabase=database.getCardById(self.myCard.tablename, self.myCard.name)
        if cardFromDatabase:
            self.frames=soundAPI.getFrames(self.myCard.pronounciation)
            self.listenButton.setEnabled(True)
        else: #this means the card was prevously deleted
            self.frames=[]
            self.createButton.setEnabled(False)
            self.deleteWidget.setEnabled(False)
            self.recordButton.setEnabled(False)
    redirect=QtCore.pyqtSignal()
    def confirmDeletion(self):
        deletionMessage = "Cette action effacera la carte '{}'. Êtes-vous certain de vouloir continuer ?".format(self.myCard.word)
        self.pop_up = pop_upWidget(self, deletionMessage, "J'en suis sûr", "Annuler")
        self.pop_up.accept.connect(self.delete)
        self.pop_up.refuse.connect(self.deletionWasCancelled)
        self.nameWidget.setVisible(False)
        self.bottomWidget.setVisible(False)
        self.answergridWidget.setVisible(False)
        self.pop_up.show()
    
    def delete(self):
        database.removeCard(self.myCard.tablename, self.myCard.name)
        self.redirect.emit()
        
    def deletionWasCancelled(self):
        self.nameWidget.setVisible(True)
        self.bottomWidget.setVisible(True)
        self.answergridWidget.setVisible(True)