# -*- coding: utf-8 -*-
#interface global à afficher à l'ouverture
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout, QCommandLinkButton, QLabel, QFrame, QToolBox, QComboBox,QShortcut 
import sys

from view import editCardsInterf, rechercheInterf, parcours, viewCard, settingsInterf, AccessSettings, languageErasure
from view.games import dragAndDrop, vraiOuFaux, hotCold, memory, pointToCard
from model import database, rechercheFonct

class Paradigme(QWidget):
    """
    this is the model that every important display has to follow:
    one short initialisation function, mainly copying the arguments,
    one "stealTheLimelight" function which makes the display appear and 
    does everything else,
    one "toTheShadows" function, which I could probably do without because it
    always calls the close method
    one "redirect" signal which is connected to the redirectDisplay of 
    WelcomeInterf. This changes the display to newDisplay.
    newDisplay can be "abort" if you don't actually want to change the display,
    or "previous" if you want to change back to the previous display
    or "home" if you want the home screen back
    """
    def __init__(self, parent, args):
        self.cartesJouees = args
        self.parent = parent
        self.nextDisplay = "abort"
        #...
    def stealTheLimelight(self):
        super(Paradigme, self).__init__(self.parent)
        # access settings
        # ...
    redirect=QtCore.pyqtSignal()
    def toTheShadows(self):
        self.close()

class FeatureButton(QCommandLinkButton):
    def __init__(self, buttonParentWindow):
        super(FeatureButton, self).__init__(buttonParentWindow)
    def init(self, language, word, viewParentWindow):
        self.viewParentWindow = viewParentWindow
        self.language = language
        self.word = word
        self.setText(word)
        self.linkedView = viewCard.viewWindow(viewParentWindow, language, word)
    def setEmpty(self):
        self.setText("...")
        self.linkedView = "abort"
    def getView(self):
        return viewCard.viewWindow(self.viewParentWindow, self.language, self.word)

## l'ecran d'accueil interne avec des onglets
class HomeScreen(QToolBox):
    def __init__(self, parentWindow, language, folderIndex=0):
        self.nextDisplay="abort"
        self.parentWindow = parentWindow
        self.language = language
        self.folderIndex=folderIndex
    def stealTheLimelight(self):
        super(HomeScreen, self).__init__(self.parentWindow)
        self.setFixedSize(self.parentWindow.frameSize())
        # onglet 1
        self.MesCartes = QWidget()
        self.MesCartes.setFixedSize(649, 401)
        #self.MesCartes.setGeometry(QtCore.QRect(0, 0, 689, 431))
        self.folders = parcours.parcoursLanguesFolder(self.MesCartes)
        self.folders.openLanguageSignal.connect(self.overviewLanguageLauncher)
        self.addItem(self.MesCartes, "")
        self.setItemText(self.indexOf(self.MesCartes),"Mes Cartes")
        # onglet 2
        self.MesJeux = parcours.parcoursIconsGame(663, 406, self.language)
        self.MesJeux.setGeometry(QtCore.QRect(0, 0, 669, 431))
        self.MesJeux.dragAndDropSignal.connect(self.dragAndDropLauncher)
        self.MesJeux.memorySignal.connect(self.memoryLauncher)
        self.MesJeux.hotAndColdSignal.connect(self.hotAndColdLauncher)
        self.MesJeux.rightWrongSignal.connect(self.rightWrongLauncher)
        self.MesJeux.pointSignal.connect(self.pointToLauncher)
        #iconesJeux = parcours.parcoursIconsGame(self.MesJeux)
        self.addItem(self.MesJeux, "")
        self.setItemText(self.indexOf(self.MesJeux), "Mes Jeux")
        # onglet 3
        self.MesParties = QWidget()
        self.MesParties.setGeometry(QtCore.QRect(0, 0, 649, 431))
        self.addItem(self.MesParties, "")
        self.setItemText(self.indexOf(self.MesParties), "Mes Parties")
        # selection de l'onglet principal
        self.setCurrentIndex(self.folderIndex)
        self.show()
    #triggers the display of all cards in a given language
    def overviewLanguageLauncher(self, language):
        self.nextDisplay = parcours.CardsOverview(self.parentWindow, language)
        self.redirect.emit()
    def dragAndDropLauncher(self):
        self.nextDisplay = dragAndDrop.DragAndDropGame(self.parentWindow, self.language)
        self.redirect.emit()
    def memoryLauncher(self):
        self.nextDisplay = memory.MemoryGame(self.parentWindow, self.language)
        self.redirect.emit()
    def hotAndColdLauncher(self):
        self.nextDisplay = hotCold.HotAndColdGame(self.parentWindow, self.language)
        self.redirect.emit()
    def pointToLauncher(self):
        self.nextDisplay = pointToCard.PointToCardGame(self.parentWindow, self.language)
        self.redirect.emit()
    def rightWrongLauncher(self):
        self.nextDisplay = vraiOuFaux.VraiFauxGame(self.parentWindow, self.language)
        self.redirect.emit()
    redirect=QtCore.pyqtSignal()
    def toTheShadows(self):
        self.folderIndex = self.currentIndex()
        self.close()

## la fenetre principale
class WelcomeInterf(QWidget):
    def __init__(self):
        # la fenetre
        super(WelcomeInterf, self).__init__()
        self.defaultLanguage = AccessSettings.readSettings("/user/default/langage").upper()
        self.username = AccessSettings.readSettings("/user/default/username")
        self.setWindowTitle("Welcome on our FlashCard program, " + self.username)
        self.setWindowIcon(QtGui.QIcon("view/icons/mole.png"))
        self.resize(936, 582)
        # le layout de la bande du haut
        self.ligneFixeWidget = QWidget(self)
        self.ligneFixeWidget.setGeometry(QtCore.QRect(10, 10, 891, 41))
        self.ligneFixe = QHBoxLayout(self.ligneFixeWidget)
        self.ligneFixe.setContentsMargins(0, 0, 0, 0)
        # la barre et le bouton de recherche
        self.searchBar = QLineEdit(self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.searchBar)
        self.searchButton = QPushButton(u"Search", self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.searchButton)
        # un espace (futur nom + logo ?)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ligneFixe.addItem(spacerItem)
        # le bouton de navigation vers l'affichage precedent
        self.previousButton = QtWidgets.QPushButton("previous",self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.previousButton)
        self.previousButton.setEnabled(False)
        # le bouton de navigation vers l'affichage suivant
        self.nextButton = QtWidgets.QPushButton("next",self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        # le bouton de creation d'une nouvelle carte
        self.newButton = QtWidgets.QPushButton(u"New Card",self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.newButton)
        # le bouton des reglages de l'application
        self.settingsButton = QtWidgets.QPushButton(u"Settings", self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.settingsButton)

        # la barre de resume sur le cote
        self.sideBanner = QGroupBox(self)
        self.sideBanner.setGeometry(QtCore.QRect(10, 60, 211, 501))
        self.barreResume = QVBoxLayout(self.sideBanner)
        # bouton d'accueil
        self.welcomeButton = QPushButton(u"Accueil", self.sideBanner)
        self.barreResume.addWidget(self.welcomeButton)
        # bouton pour effacer un langage
        self.eraseButton = QPushButton(u"Erase Language", self.sideBanner)
        self.barreResume.addWidget(self.eraseButton)
        #bouton de language
        self.editLanguage = QComboBox(self.sideBanner)
        self.langues = database.giveAllLanguages()
        for i in range(len(self.langues)):
            self.editLanguage.addItem(self.langues[i])
            if self.langues[i] == self.defaultLanguage:
                self.editLanguage.setCurrentIndex(i)
        self.barreResume.addWidget(self.editLanguage)
        self.Table=self.editLanguage.currentText()
        # une ligne de separation horizontale
        self.line1 = QFrame(self.sideBanner)
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.barreResume.addWidget(self.line1)
        self.featureButtons=[FeatureButton(self.sideBanner) for i in range(9)]
        self.barreResume.addWidget(QLabel("  Cards to learn", self.sideBanner))
        for i in range(0, 3):
            self.barreResume.addWidget(self.featureButtons[i])
        self.barreResume.addWidget(QLabel("  Cards to go over", self.sideBanner))
        for i in range(3, 6):
            self.barreResume.addWidget(self.featureButtons[i])
        self.barreResume.addWidget(QLabel("  Cards known", self.sideBanner))
        for i in range(6, 9):
            self.barreResume.addWidget(self.featureButtons[i])
        #main screen
        self.screen = QWidget(self)
        self.screen.setGeometry(QtCore.QRect(230, 60, 671, 501))
        self.initWithHomeScreen()
        self.setFeatureButtons()
        
        #_____________________signals and slots___________________________#
#        for i in range(0, 9):
#            self.featureButtons[i].clicked.connect( lambda x:self.changeDisplay(self.featureButtons[i].linkedView))
        self.featureButtons[0].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[0].linkedView))
        self.featureButtons[1].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[1].linkedView))
        self.featureButtons[2].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[2].linkedView))
        self.featureButtons[3].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[3].linkedView))
        self.featureButtons[4].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[4].linkedView))
        self.featureButtons[5].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[5].linkedView))
        self.featureButtons[6].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[6].linkedView))
        self.featureButtons[7].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[7].linkedView))
        self.featureButtons[8].clicked.connect(lambda x:self.changeDisplay(self.featureButtons[8].linkedView))
        self.welcomeButton.clicked.connect(lambda x:self.changeDisplay(HomeScreen(self.screen, self.editLanguage.currentText())))
        self.previousButton.clicked.connect(self.backToPreviousDisplay)
        self.nextButton.clicked.connect(self.backToNextDisplay)
        self.newButton.clicked.connect(lambda x:self.changeDisplay(editCardsInterf.CardCreation(self.screen, self.history[self.historyIndex], self.Table)))
        self.settingsButton.clicked.connect(lambda x:self.changeDisplay(settingsInterf.mySettings(self.screen, self.history[self.historyIndex])))
        self.editLanguage.activated.connect(self.changeLanguage)
        self.searchButton.clicked.connect(self.quickSearch)
        self.eraseButton.clicked.connect(self.eraseLanguage)
        
        #___________________shortcuts_____________________________________#
        self.closeShortcut=QShortcut(QtGui.QKeySequence('Ctrl+w'), self)
        self.closeShortcut.activated.connect(self.close)

    def setFeatureButtons(self):
        cardsToLearn=database.getCardsToLearn(self.Table,0,4)
        cardsToGoOver=database.getCardsToLearn(self.Table,5,9)
        cardsKnown=database.getCardsToLearn(self.Table,10,10)
        i=0
        while i < 3:
            if i < len(cardsToLearn):
                self.featureButtons[i].init(self.Table, cardsToLearn[i].word, self.screen)
            else:
                self.featureButtons[i].setEmpty()
            i+=1
        while i < 6:
            if i - 3 < len(cardsToGoOver):
                self.featureButtons[i].init(self.Table, cardsToGoOver[i-3].word, self.screen)
            else:
                self.featureButtons[i].setEmpty()
            i+=1
        while i < 9:
            if i - 6 < len(cardsKnown):
                self.featureButtons[i].init(self.Table, cardsKnown[i-6].word, self.screen)
            else:
                self.featureButtons[i].setEmpty()
            i+=1
    def initWithHomeScreen(self):
        self.history = [HomeScreen(self.screen, self.editLanguage.currentText())]
        self.historyIndex = 0
        self.history[self.historyIndex].stealTheLimelight()
        self.history[self.historyIndex].redirect.connect(self.redirectDisplay)
    def changeLanguage(self):
        if self.Table==self.editLanguage.currentText():
            return
        self.Table=self.editLanguage.currentText()
        self.history[self.historyIndex].toTheShadows()
        self.initWithHomeScreen()
        self.setFeatureButtons()
        self.previousButton.setEnabled(False)
        self.nextButton.setEnabled(False)
    def eraseLanguage(self):
        self.changeDisplay(languageErasure.eraseLanguageInterf(self.screen))
    def quickSearch(self):
        searchResult=rechercheFonct.recherche(self.Table, self.searchBar.text(), '', '', '', True)
        if searchResult:
            self.changeDisplay(parcours.CardsOverview(self.screen, searchResult))
        
    #_________________________Display_Control______________________________#
    #this is for when you know what display you want
    def changeDisplay(self, newDisplay):
        if newDisplay == "abort":
            print("aborting change of display")
            return
        if newDisplay == "previous":
            newDisplay = self.history[self.historyIndex - 1]
        if newDisplay == "home":
            newDisplay = HomeScreen(self.screen, self.editLanguage.currentText())
        while self.historyIndex < len(self.history) - 1:
            self.history.pop()
        self.history[self.historyIndex].toTheShadows()
        newDisplay.stealTheLimelight()
        self.historyIndex = len(self.history)
        self.history.append(newDisplay)
        newDisplay.redirect.connect(self.redirectDisplay)
        self.previousButton.setEnabled(True)
        self.nextButton.setEnabled(False)
    #this is for when a display is making you move to another display
    def redirectDisplay(self):
        self.changeDisplay(self.history[self.historyIndex].nextDisplay)
    #this is for fluid navigation among past displays
    def backToPreviousDisplay(self):
        self.history[self.historyIndex].toTheShadows()
        self.history[self.historyIndex-1].stealTheLimelight()
        self.historyIndex-=1
        self.history[self.historyIndex].redirect.connect(self.redirectDisplay)
        if self.historyIndex == 0:
            self.previousButton.setEnabled(False)
        self.nextButton.setEnabled(True)
    def backToNextDisplay(self):
        self.history[self.historyIndex].toTheShadows()
        self.history[self.historyIndex+1].stealTheLimelight()
        self.historyIndex+=1
        self.history[self.historyIndex].redirect.connect(self.redirectDisplay)
        if self.historyIndex==len(self.history)-1:
            self.nextButton.setEnabled(False)
        self.previousButton.setEnabled(True)