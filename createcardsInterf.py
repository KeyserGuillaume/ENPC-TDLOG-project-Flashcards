############# definition de l'interface de creation de flash cards

import flashcard, database

## a aller récupérer dans une base de donnée plus tard
## toutes les langues prises en charges
langues = database.giveAllLanguages()  # ["anglais", "other"]
# les classes grammaticales dispo (definitif)
natureGram = ["noun", "adjective", "verbe", "adverbe", "pronoun", "preposition", "conjunction", "interjection",
              "determiner", "other"]

#from PyQt4.QtGui import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox, QFileDialog
#from PyQt4 import QtCore

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, \
    QProgressBar, QSlider, QComboBox, QFileDialog, QFrame

import sys

class pop_upWidget(QWidget):
    def __init__(self, parent, queryText, yesText, noText):
        super().__init__(parent)
        self.resize(451, 80)
#        self.setAutoFillBackground(True)
#        self.col = QtGui.QColor(255, 255, 255)
#        self.setStyleSheet("QWidget { background-color: %s }" %  
#            self.col.name())
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
        fileName, _ = QFileDialog.getOpenFileName(self, "Select your file", "",
                                                  "Image Files (*.png *.jpg *.jp2 *.bmp *.tiff *.xpm *.gif *.webp *.eps);;Sound Files (*.mp3 *.wav *.m4a *.aac *.aiff *.gsm *.m4p *.wma);;All Files (*)",
                                                  options=options)
        if fileName:
            self._myname = fileName

    @property
    def name(self):
        return self._myname


class CardCreation(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.mynature.setText(" Selectionez la nature du mot :")
        self.editnature = QComboBox(self.answergridWidget)
        self.answergrid.addWidget(self.editnature, 8, 1, 1, 1)
        for naturespossibles in natureGram:
            self.editnature.addItem(naturespossibles)
        # ligne 9 : indiquer la langue
        self.mylanguage = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mylanguage, 9, 0, 1, 1)
        self.mylanguage.setText(" Selectionez la langue :")
        self.editlanguage = QComboBox(self.answergridWidget)
        self.answergrid.addWidget(self.editlanguage, 9, 1, 1, 1)
        for languespossibles in langues:
            self.editlanguage.addItem(languespossibles)
        self.editlanguage.addItem("Other")
        # ligne 10 : entrer une nouvelle langue
        self.myLanguage = QLabel(self.answergridWidget)
        self.myLanguage.setText(" Definissez la nouvelle langue :")
        self.answergrid.addWidget(self.myLanguage, 10, 0, 1, 1)
        self.setLanguage = QLineEdit(self.answergridWidget)
        self.answergrid.addWidget(self.setLanguage, 10, 1, 1, 1)
        self.setLanguage.setEnabled(False)
        # ligne 11 : charge une image
        self.myillustration = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.myillustration, 11, 0, 1, 1)
        self.myillustration.setText(" Selectionez une image :")
        self.chooseButton1 = QPushButton(u"Choisir", self.answergridWidget)
        self.answergrid.addWidget(self.chooseButton1, 11, 1, 1, 1)
        self.image = ""
        # ligne 12 : charger un fichier son de prononciation
        self.mysound = QLabel(self.answergridWidget)
        self.answergrid.addWidget(self.mysound, 12, 0, 1, 1)
        self.mysound.setText(" Selectionez une prononciation :")
        self.chooseButton2 = QPushButton(u"Choisir", self.answergridWidget)
        self.answergrid.addWidget(self.chooseButton2, 12, 1, 1, 1)
        self.sound = ""

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
        # barre de progression indiquant a quel point la carte est complete
        self.progress = 0  # niveau de progres de le remplissage de la carte
        self.progressBar = QProgressBar(self.bottomWidget)
        self.progressBar.setProperty("value", self.progress)
        self.tocreate.addWidget(self.progressBar)
        # bouton de creation
        self.createButton = QPushButton(u"Create", self.bottomWidget)
        self.tocreate.addWidget(self.createButton)

        ## gestion des slots et signaux
        # fenetre de dialogue pour la selection d'un fichier
        self.chooseButton1.clicked.connect(self.browse1)
        self.chooseButton2.clicked.connect(self.browse2)
        # creation d'une carte
        self.createButton.clicked.connect(self.commit)
        # mise a jour du progres
        self.setname.textEdited.connect(self.progression)
        self.editword.editingFinished.connect(self.progression)
        self.edittrad.editingFinished.connect(self.progression)
        self.editexample.editingFinished.connect(self.progression)
        self.editthema.editingFinished.connect(self.progression)
        self.editlanguage.activated.connect(self.languageChosen)
        self.setLanguage.editingFinished.connect(self.newLanguage)
        # self.editdifficult.textEdited.connect(self.progression)
        # self.editproficiency.textEdited.connect(self.progression)
    created=QtCore.pyqtSignal()
    def progression(self):
        self.progress += 12
        self.progress = min(self.progress, 100)
        self.progressBar.setProperty("value", self.progress)

    def languageChosen(self):
        langue = str(self.editlanguage.currentText())
        if (langue == "Other"):
            self.setLanguage.setEnabled(True)
            return
        self.setname.setText(str(database.giveNewCardName(langue)))

    def newLanguage(self):
        self.setname.setText("1")

    def browse1(self):
        ex = SearchDirectory()
        self.image = ex.name

    def browse2(self):
        ex = SearchDirectory()
        self.sound = ex.name

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

def createNewCard():
    args = sys.argv
    a = QApplication(args)
    w=QWidget()
    w.resize(497, 492)
    mf = CardCreation(w)
    mf.created.connect(w.close)
    w.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)
    # mf.quit()
    # sys.exit(a.exec_())

class CardModification(CardCreation):
    def __init__(self, parent, mycard):
        super().__init__(parent)
        self.myCard=mycard
        # remplissage avec les data existantes
        self.editword.setText(mycard.word)
        self.editword.setEnabled(False)
        self.edittrad.setText(mycard.trad)
        self.editexample.setText(mycard.exemple)
        self.editthema.setText(mycard.thema)
        self.editdifficult.setValue(mycard.howhard * 10)
        self.editproficiency.setValue(mycard.level * 10)
        self.editlanguage.setCurrentText(mycard.tablename)
        self.editlanguage.setEnabled(False)
        self.editnature.setCurrentText(mycard.nature)
        self.setname.setText(str(mycard.name))
        self.createButton.setText("Modify")
        self.progressBar.setVisible(False)
        self.deleteWidget=QPushButton("delete", self.bottomWidget)
        self.tocreate.addWidget(self.deleteWidget)
        self.bottomWidget.resize(self.bottomWidget.sizeHint())
        self.deleteWidget.clicked.connect(self.confirmDeletion)
    deleted=QtCore.pyqtSignal()
    modified=QtCore.pyqtSignal()
    def confirmDeletion(self):
        self.pop_up = pop_upWidget(self, "Cette action effacera la carte '{}'. Êtes-vous certain de vouloir continuer ?".format(self.myCard.word), "J'en suis sûr", "Annuler")
        self.pop_up.accept.connect(self.delete)
        self.pop_up.refuse.connect(self.deletionWasCancelled)
        self.nameWidget.setVisible(False)
        self.bottomWidget.setVisible(False)
        self.answergridWidget.setVisible(False)
#        self.col = QtGui.QColor(255, 255, 255)
#        self.setStyleSheet("QWidget { background-color: %s }" %  
#            self.col.name())
        self.pop_up.show()
    
    def delete(self):
        database.removeCard(self.myCard.tablename, self.myCard.name)
        self.deleted.emit()
        self.close()
        
    def deletionWasCancelled(self):
        self.nameWidget.setVisible(True)
        self.bottomWidget.setVisible(True)
        self.answergridWidget.setVisible(True)


def modifyCard(mycard):
    args = sys.argv
    b = QApplication(args)
    w=QWidget()
    w.setFixedSize(497, 492)
    mf = CardModification(w, mycard)
    mf.modified.connect(w.close)
    mf.deleted.connect(w.close)
    w.show()
    b.exec_()
    b.lastWindowClosed.connect(b.quit)

if __name__ == "__main__":
    #createNewCard()
    mycard = database.getCardById("anglais", database.getRandomCard("anglais"))
    print(mycard)
    modifyCard(mycard)

