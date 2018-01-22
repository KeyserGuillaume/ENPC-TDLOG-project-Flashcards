#interface global à afficher à l'ouverture
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout, QCommandLinkButton, QLabel, QFrame, QToolBox, QComboBox,QShortcut 
import sys

import createcardsInterf, database, flashcard, rechercheInterf, parcours, viewCard, dragAndDrop, vraiOuFaux, hotColdGame, memory, pointToCard


### traitement des listes d'apprentissage
#Table='anglais'
## entre 0 et 4
#cardsToLearn=database.getCardsToLearn(Table,0,4)
##cardsToLearn=["suspendre","remuer","..."]
# # entre 5 et 9
#cardsToGoOver=database.getCardsToLearn(Table,5,9)
##cardsToGoOver=["echarpe","amour", "..."]
## 10
#cardsKnown=database.getCardsToLearn(Table,10,10)
##cardsKnown=["bonjour","bienvenue", "..."]


### les boutons de commande connectés a l'interface de lecture
## gere quand les listes contiennent moins de 3 items (len<3)
#openFunction contient la fonction qui doit etre appelee qd le
#connectedButton est active
class ConnectedButton(QCommandLinkButton):
    def __init__(self, cardlist, rank, place, name, openFunction):
        self.cardlist=cardlist
        self.rank=rank
        self.rank_orig=self.rank
        super(ConnectedButton, self).__init__(place)
        self.openInterfFunction=openFunction
        self.init()
    def init(self):
        if len(self.cardlist) == 0 : ## pas assez d'elements dans la liste
           self.rank=3
        if len(self.cardlist) == 1 and self.rank>0 : ## pas assez d'elements dans la liste
           self.rank=3
        if len(self.cardlist) == 2 and self.rank>1 : ## pas assez d'elements dans la liste
            self.rank = 3

        if self.rank<=1:
            self.setText(self.cardlist[self.rank].word)
        else:
            self.setText("...")
    def open(self):
        if self.rank<3:
            # ouverture de l interface de lecture de cartes
            self.openInterfFunction(self.rank, self.cardlist)
    def changeCardList(self, cardlist):
        self.cardlist=cardlist
        self.rank=self.rank_orig
        self.init()

## l'ecran d'accueil interne avec des onglets
class HomeScreen(QToolBox):
    def __init__(self, givenLayout, language):
        super(HomeScreen, self).__init__(givenLayout)
        self.language=language
        self.setFixedSize(givenLayout.frameSize())
        # onglet 1
        self.MesCartes = QWidget()
        self.MesCartes.setFixedSize(649, 401)
        #self.MesCartes.setGeometry(QtCore.QRect(0, 0, 689, 431))
        self.folders = parcours.parcoursLanguesFolder(self.MesCartes)
        self.folders.openLanguageSignal.connect(self.openLanguageSignal.emit)
        self.addItem(self.MesCartes, "")
        self.setItemText(self.indexOf(self.MesCartes),"Mes Cartes")
        # onglet 2
        self.MesJeux = parcours.parcoursIconsGame(663, 406, self.language)
        self.MesJeux.setGeometry(QtCore.QRect(0, 0, 669, 431))
        self.MesJeux.dragAndDropSignal.connect(self.dragAndDropSignal.emit)
        self.MesJeux.memorySignal.connect(self.memorySignal.emit)
        self.MesJeux.hotAndColdSignal.connect(self.hotAndColdSignal.emit)
        self.MesJeux.rightWrongSignal.connect(self.rightWrongSignal.emit)
        self.MesJeux.pointSignal.connect(self.pointSignal.emit)
        #iconesJeux = parcours.parcoursIconsGame(self.MesJeux)
        self.addItem(self.MesJeux, "")
        self.setItemText(self.indexOf(self.MesJeux), "Mes Jeux")
        # onglet 3
        self.MesParties = QWidget()
        self.MesParties.setGeometry(QtCore.QRect(0, 0, 649, 431))
        self.addItem(self.MesParties, "")
        self.setItemText(self.indexOf(self.MesParties), "Mes Parties")
        # selection de l'onglet principal
        self.setCurrentIndex(0)
        self.closeShortcut=QShortcut(QtGui.QKeySequence('Ctrl+c'), self)
        self.closeShortcut.activated.connect(self.close)
    openLanguageSignal=QtCore.pyqtSignal(str)
    dragAndDropSignal=QtCore.pyqtSignal()    
    memorySignal=QtCore.pyqtSignal()
    hotAndColdSignal=QtCore.pyqtSignal()
    pointSignal=QtCore.pyqtSignal()
    rightWrongSignal=QtCore.pyqtSignal()
    
        
    #un peu alambique : pour fermer, on cache ongletsAccueil
    def close(self):
        self.setVisible(False)

## la fenetre principale
class WelcomeInterf(object):
    def __init__(self):
        # la fenetre
        self.Dialog = QWidget()
        self.Dialog.setWindowTitle("Welcome on our FlashCard program")
        self.Dialog.resize(936, 582)
        # le layout de la bande du haute
        self.ligneFixeWidget = QWidget(self.Dialog)
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
        # le bouton de modification
        # ne peut pas ouvrir directement l'interface de modification car il faut sélectioner une carte
        self.modifyButton = QPushButton(u"Modify", self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.modifyButton)
        # le bouton d'mportation / exportation
        # pas encore gere non plus ; a venir ?
        self.importButton = QtWidgets.QPushButton(u"Import",self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.importButton)
        self.importButton.setEnabled(False)
        # le bouton de creation d'une nouvelle carte
        self.newButton = QtWidgets.QPushButton(u"New Card",self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.newButton)
        # le bouton des réglages de l'application
        # pas encore pris en compte
        self.settingsButton = QtWidgets.QPushButton(u"Settings", self.ligneFixeWidget)
        self.ligneFixe.addWidget(self.settingsButton)
        self.settingsButton.setEnabled(False)

        # la barre de resume sur le cote
        self.ResumeBox = QGroupBox(self.Dialog)
        self.ResumeBox.setGeometry(QtCore.QRect(10, 60, 211, 501))
        self.barreResume = QVBoxLayout(self.ResumeBox)
        # bouton d'accueil
        # determiner quel affichage
        self.accueil = QPushButton(u"Accueil", self.ResumeBox)
        self.barreResume.addWidget(self.accueil)
        self.accueil.setEnabled(True)
        #bouton de language
        self.editlanguage = QComboBox(self.ResumeBox)
        self.langues = database.giveAllLanguages()
        for languespossibles in self.langues:
            self.editlanguage.addItem(languespossibles)        
        self.barreResume.addWidget(self.editlanguage)
        self.Table=self.editlanguage.currentText()
        self.getCards()
        # bouton de profil utilisateur
        # non pris en compte
        #self.profil = QPushButton(u"User profile", self.ResumeBox)
        #self.barreResume.addWidget(self.profil)
        #self.profil.setEnabled(False)
        # une ligne de séparation horizontale
        self.line1 = QFrame(self.ResumeBox)
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.barreResume.addWidget(self.line1)
        # label cartes a apprendre et les 3 boutons carte associés
        self.learnlabel = QLabel(self.ResumeBox)
        self.learnlabel.setText("  Cards to learn")
        self.barreResume.addWidget(self.learnlabel)
        self.learn1 = ConnectedButton(self.cardsToLearn, 0, self.ResumeBox, "learn1", self.openViewCards)
        self.barreResume.addWidget(self.learn1)
        self.learn2 = ConnectedButton(self.cardsToLearn, 1, self.ResumeBox, "learn2", self.openViewCards)
        self.barreResume.addWidget(self.learn2)
        self.learn3 = ConnectedButton(self.cardsToLearn, 2, self.ResumeBox, "learn3", self.openViewCards)
        self.barreResume.addWidget(self.learn3)
        # label cartes a revoir et les 3 boutons carte associés
        self.overlabel = QLabel(self.ResumeBox)
        self.overlabel.setText("  Cards to go over")
        self.barreResume.addWidget(self.overlabel)
        self.over1 = ConnectedButton(self.cardsToGoOver, 0, self.ResumeBox, "over1", self.openViewCards)
        self.barreResume.addWidget(self.over1)
        self.over2 = ConnectedButton(self.cardsToGoOver, 1, self.ResumeBox, "over2", self.openViewCards)
        self.barreResume.addWidget(self.over2)
        self.over3 = ConnectedButton(self.cardsToGoOver, 2, self.ResumeBox, "over3", self.openViewCards)
        self.barreResume.addWidget(self.over3)
        # label cartes bien connues et les 3 boutons carte associés
        self.knowledgelabel = QLabel(self.ResumeBox)
        self.knowledgelabel.setText("  Cards known")
        self.barreResume.addWidget(self.knowledgelabel)
        self.know1 = ConnectedButton(self.cardsKnown, 0, self.ResumeBox, "know1", self.openViewCards)
        self.barreResume.addWidget(self.know1)
        self.know2 = ConnectedButton(self.cardsKnown, 1, self.ResumeBox, "know2", self.openViewCards)
        self.barreResume.addWidget(self.know2)
        self.know3 = ConnectedButton(self.cardsKnown, 2, self.ResumeBox, "know3", self.openViewCards)
        self.barreResume.addWidget(self.know3)
        # une ligne de séparation horizontale
        self.line2 = QFrame(self.ResumeBox)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.barreResume.addWidget(self.line2)
        # le bouton d'aideopenCardSignal=QtCore.pyqtSignal(str, int)
        self.helpButton = QPushButton(u"Help", self.ResumeBox)
        self.barreResume.addWidget(self.helpButton)
        self.helpButton.setEnabled(False)

        ## ecran central changeant
        # au moment de l'ouverture ecran d'accueil
        # plus tard interface de parcours de carte, de lecture de cartes,
        # de jeu et de parcours de jeu
        ### le layout central avec les onglets
        self.screenLayout = QWidget(self.Dialog)
        self.screenLayout.setGeometry(QtCore.QRect(230, 60, 671, 501))
        self.myscreen=HomeScreen(self.screenLayout, self.editlanguage.currentText())

        #raccourcis
        self.closeShortcut=QShortcut(QtGui.QKeySequence('Ctrl+c'), self.Dialog)
        
        ## gestion des slots et des signaux
        self.createInterf=None
        self.newButton.clicked.connect(self.createnew)
        self.accueil.clicked.connect(self.retourAccueil)
        self.selectedcard=None
        self.modifInterf=None
        self.modifyButton.clicked.connect(self.modifycard)
        self.searchInterf = None
        self.currentScreen=self.myscreen
        self.searchButton.clicked.connect(self.search)
        self.learn1.clicked.connect(self.learn1.open)
        self.learn2.clicked.connect(self.learn2.open)
        self.learn3.clicked.connect(self.learn3.open)
        self.over1.clicked.connect(self.over1.open)
        self.over2.clicked.connect(self.over2.open)
        self.over3.clicked.connect(self.over3.open)
        self.know1.clicked.connect(self.know1.open)
        self.know2.clicked.connect(self.know2.open)
        self.know3.clicked.connect(self.know3.open)
        self.closeShortcut.activated.connect(self.Dialog.close)
        self.editlanguage.activated.connect(self.changeLanguage)
        self.myscreen.dragAndDropSignal.connect(self.openDragAndDrop)
        self.myscreen.hotAndColdSignal.connect(self.openHotAndCold)
        self.myscreen.openLanguageSignal.connect(self.openParcours)
        self.myscreen.rightWrongSignal.connect(self.openVraiOuFaux)
        self.myscreen.memorySignal.connect(self.openMemory)
        self.myscreen.pointSignal.connect(self.openPointTo)
        
    def changeLanguage(self):
        self.Table=self.editlanguage.currentText()
        self.getCards()
        self.myscreen.language=self.Table
        self.myscreen.MesJeux.language=self.Table
        self.learn1.changeCardList(self.cardsToLearn)
        self.learn2.changeCardList(self.cardsToLearn)
        self.learn3.changeCardList(self.cardsToLearn)
        self.over1.changeCardList(self.cardsToGoOver)
        self.over2.changeCardList(self.cardsToGoOver)
        self.over3.changeCardList(self.cardsToGoOver)
        self.know1.changeCardList(self.cardsKnown)
        self.know2.changeCardList(self.cardsKnown)
        self.know3.changeCardList(self.cardsKnown)
        
    def getCards(self):
        self.cardsToLearn=database.getCardsToLearn(self.Table,0,4)
        self.cardsToGoOver=database.getCardsToLearn(self.Table,5,9)
        print([x.word for x in self.cardsToGoOver])
        self.cardsKnown=database.getCardsToLearn(self.Table,10,10)
    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def retourAccueil(self):
        self.currentScreen.close()
        self.currentScreen=self.myscreen
        self.displayHomeScreen()
    def createnew(self):
        # ouverture de l'interface de creation
        self.currentScreen.close()
        self.createInterf = createcardsInterf.CardCreation(self.screenLayout)
        self.currentScreen = self.createInterf
        self.createInterf.show()
        self.createInterf.created.connect(self.displayHomeScreen)
    def modifycard(self):
        # la carte pour l'instant random
        self.selectedcard=database.getCardById("anglais", database.getRandomCard("anglais"))
        # ouverture de l'interface de modification
        self.modifInterf=createcardsInterf.CardModification(self.screenLayout, self.selectedcard)
        #on cache l'ecran d'accueil
        self.currentScreen.close()
        self.currentScreen = self.modifInterf
        self.modifInterf.show()
        self.modifInterf.modified.connect(self.displayHomeScreen)
        self.modifInterf.deleted.connect(self.displayHomeScreen)
    def openParcours(self, language):
        self.currentScreen.close()
        self.parcoursInterf=parcours.parcoursChosenCards(self.screenLayout, language)
        self.currentScreen=self.parcoursInterf
        self.currentScreen.show()
        self.parcoursInterf.openCardSignal.connect(self.openCard)
    def openCard(self,language, rank):
        self.openViewCards(rank, database.getAllCards(language))
    def openDragAndDrop(self):
        self.currentScreen.close()
        self.DDInterf = dragAndDrop.dragDropGame(self.screenLayout, database.getCardsToLearn(self.Table,0,10)[0:16])
        self.DDInterf.show()
        self.currentScreen=self.DDInterf
        self.DDInterf.leave.connect(self.displayHomeScreen)
    def openHotAndCold(self):
        self.currentScreen.close()
        self.HCInterf = hotColdGame.hotColdGame(self.screenLayout, database.getCardsToLearn(self.Table,0,10)[0:20])
        self.HCInterf.show()
        self.currentScreen=self.HCInterf
        self.HCInterf.leave.connect(self.displayHomeScreen)
    def openVraiOuFaux(self):
        self.currentScreen.close()
        self.VFInterf = vraiOuFaux.vraiFauxGame(self.screenLayout, database.getCardsToLearn(self.Table,0,10)[0:25])
        self.VFInterf.show()
        self.currentScreen = self.VFInterf
        self.VFInterf.leave.connect(self.displayHomeScreen) 
    def openViewCards(self, rank, cardlist):
        self.currentScreen.close()
        self.linkedInterf = viewCard.viewDialog(self.screenLayout, rank, cardlist)
        self.linkedInterf.show()
        self.currentScreen=self.linkedInterf
    def openMemory(self):
        self.currentScreen.close()
        self.MemoryInterf = memory.MemoryGameWindow(self.screenLayout, database.getCardsToLearn(self.Table,0,10)[0:12])
        self.MemoryInterf.show()
        self.currentScreen=self.MemoryInterf
        self.MemoryInterf.leave.connect(self.displayHomeScreen)
    def openPointTo(self):
        self.currentScreen.close()
        self.PointToInterf = pointToCard.pointToCardGame(self.screenLayout, database.getCardsToLearn(self.Table,0,10)[0:20])
        self.PointToInterf.show()
        self.currentScreen=self.PointToInterf
        self.PointToInterf.leave.connect(self.displayHomeScreen)
    def displayHomeScreen(self):
        self.getCards()
        self.myscreen.setVisible(True)
        self.currentScreen=self.myscreen
    def search(self):
        self.searchInterf = rechercheInterf.Recherche()
        tosearch=self.searchBar.text()
        self.searchInterf.lineE_mot.setText(tosearch)
        self.searchInterf.click_btn_lancer()
        self.searchInterf.show()

if __name__ == "__main__":
    args = sys.argv
    a = QApplication(args)
    mf = WelcomeInterf()
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)
    # sys.exit(a.exec_())
