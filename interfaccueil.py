#interface global à afficher à l'ouverture
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout, QCommandLinkButton, QLabel, QFrame, QToolBox
import sys

import createcardsInterf, database, flashcard, rechercheInterf, parcours, viewCard, dragAndDrop


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
class ConnectedButton(QCommandLinkButton):
    def __init__(self, cardlist, rank, place, name):
        self.cardlist=cardlist
        self.rank=rank
        super(ConnectedButton, self).__init__(place)
        self.setObjectName(name)
        self.LinkedInterf = None
        if len(self.cardlist) == 0 : ## pas assez d'elements dans la liste
           self.rank=3
        if len(self.cardlist) == 1 and rank>0 : ## pas assez d'elements dans la liste
           self.rank=3
        if len(self.cardlist) == 2 and rank>1 : ## pas assez d'elements dans la liste
            self.rank = 3

        if self.rank<=1:
            self.setText(cardlist[self.rank].word)
        else:
            self.setText("...")

    def open(self):
        if self.rank<3:
            # ouverture de l interface de lecture de cartes
            self.LinkedInterf = viewCard.ViewDialog(self.rank, self.cardlist)
            self.LinkedInterf.show()

## l'ecran d'accueil interne avec des onglets
class HomeScreen(QToolBox):
    def __init__(self, givenLayout):
        super(HomeScreen, self).__init__(givenLayout)
        self.setFixedSize(givenLayout.frameSize())
        self.setObjectName("ongletsAccueil")
        # onglet 1
        self.MesCartes = QWidget()
        self.MesCartes.setFixedSize(649, 401)
        #self.MesCartes.setGeometry(QtCore.QRect(0, 0, 689, 431))
        self.MesCartes.setObjectName("MesCartes")
        folders = parcours.parcoursLanguesFolder(self.MesCartes)
        self.w1=QWidget()
        #self.addItem(self.w1, "")
        #self.setItemText(0, "w1")
        self.addItem(self.MesCartes, "")
        self.setItemText(self.indexOf(self.MesCartes),"Mes Cartes")
        # onglet 2
        #self.MesJeux = QWidget()
        self.MesJeux = parcours.parcoursIconsGame(663, 406)
        self.MesJeux.setGeometry(QtCore.QRect(0, 0, 669, 431))
        self.MesJeux.setObjectName("MesJeux")
        self.MesJeux.dragAndDropSignal.connect(self.dragAndDropSignal.emit)
        #iconesJeux = parcours.parcoursIconsGame(self.MesJeux)        
        self.w2=QWidget()
        #self.addItem(self.w2, "")
        #self.setItemText(1, "w2")
        self.addItem(self.MesJeux, "")
        self.setItemText(self.indexOf(self.MesJeux), "Mes Jeux")
        # onglet 3
        self.MesParties = QWidget()
        self.MesParties.setGeometry(QtCore.QRect(0, 0, 649, 431))
        self.MesParties.setObjectName("MesParties")
        self.w3=QWidget()
        #self.addItem(self.w3, "")
        #self.setItemText(2, "w3")
        self.addItem(self.MesParties, "")
        self.setItemText(self.indexOf(self.MesParties), "Mes Parties")
        # selection de l'onglet principal
        self.setCurrentIndex(0)
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
        self.Table='anglais'
        self.getCards()
        # la fenetre
        self.Dialog = QWidget()
        self.Dialog.setObjectName("Welcome")
        self.Dialog.setWindowTitle("Welcome on our FlashCard program")
        self.Dialog.resize(936, 582)
        # le layout de la bande du haute
        self.ligneFixeWidget = QWidget(self.Dialog)
        self.ligneFixeWidget.setGeometry(QtCore.QRect(10, 10, 891, 41))
        self.ligneFixeWidget.setObjectName("ligneFixeWidget")
        self.ligneFixe = QHBoxLayout(self.ligneFixeWidget)
        self.ligneFixe.setContentsMargins(0, 0, 0, 0)
        self.ligneFixe.setObjectName("ligneFixe")
        # la barre et le bouton de recherche
        self.searchBar = QLineEdit(self.ligneFixeWidget)
        self.searchBar.setObjectName("searchBar")
        self.ligneFixe.addWidget(self.searchBar)
        self.searchButton = QPushButton(u"Search", self.ligneFixeWidget)
        self.searchButton.setObjectName("searchButton")
        self.ligneFixe.addWidget(self.searchButton)
        # un espace (futur nom + logo ?)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ligneFixe.addItem(spacerItem)
        # le bouton de modification
        # ne peut pas ouvrir directement l'interface de modification car il faut sélectioner une carte
        self.modifyButton = QPushButton(u"Modify", self.ligneFixeWidget)
        self.modifyButton.setObjectName("modifyButton")
        self.ligneFixe.addWidget(self.modifyButton)
        # le bouton d'mportation / exportation
        # pas encore gere non plus ; a venir ?
        self.importButton = QtWidgets.QPushButton(u"Import",self.ligneFixeWidget)
        self.importButton.setObjectName("importButton")
        self.ligneFixe.addWidget(self.importButton)
        self.importButton.setEnabled(False)
        # le bouton de creation d'une nouvelle carte
        self.newButton = QtWidgets.QPushButton(u"New Card",self.ligneFixeWidget)
        self.newButton.setObjectName("newButton")
        self.ligneFixe.addWidget(self.newButton)
        # le bouton des réglages de l'application
        # pas encore pris en compte
        self.settingsButton = QtWidgets.QPushButton(u"Settings", self.ligneFixeWidget)
        self.settingsButton.setObjectName("settingsButton")
        self.ligneFixe.addWidget(self.settingsButton)
        self.settingsButton.setEnabled(False)

        # la barre de resume sur le cote
        self.ResumeBox = QGroupBox(self.Dialog)
        self.ResumeBox.setGeometry(QtCore.QRect(10, 60, 211, 501))
        self.ResumeBox.setObjectName("ResumeBox")
        self.barreResume = QVBoxLayout(self.ResumeBox)
        self.barreResume.setObjectName("barreResume")
        # bouton d'accueil
        # determiner quel affichage
        self.accueil = QPushButton(u"Accueil", self.ResumeBox)
        self.accueil.setObjectName("accueil")
        self.barreResume.addWidget(self.accueil)
        self.accueil.setEnabled(True)
        # bouton de profil utilisateur
        # non pris en compte
        self.profil = QPushButton(u"User profile", self.ResumeBox)
        self.profil.setObjectName("profil")
        self.barreResume.addWidget(self.profil)
        self.profil.setEnabled(False)
        # une ligne de séparation horizontale
        self.line1 = QFrame(self.ResumeBox)
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setObjectName("separation line n1")
        self.barreResume.addWidget(self.line1)
        # label cartes a apprendre et les 3 boutons carte associés
        self.learnlabel = QLabel(self.ResumeBox)
        self.learnlabel.setObjectName("learnlabel")
        self.learnlabel.setText("  Cards to learn")
        self.barreResume.addWidget(self.learnlabel)
        self.learn1 = ConnectedButton(self.cardsToLearn, 0, self.ResumeBox, "learn1")
        self.barreResume.addWidget(self.learn1)
        self.learn2 = ConnectedButton(self.cardsToLearn, 1, self.ResumeBox, "learn2")
        self.barreResume.addWidget(self.learn2)
        self.learn3 = ConnectedButton(self.cardsToLearn, 2, self.ResumeBox, "learn3")
        self.barreResume.addWidget(self.learn3)
        # label cartes a revoir et les 3 boutons carte associésAttributeError: 'PyQt5.QtCore.pyqtSignal' object has no attribute 'connect'
        self.overlabel = QLabel(self.ResumeBox)
        self.overlabel.setObjectName("overlabel")
        self.overlabel.setText("  Cards to go over")
        self.barreResume.addWidget(self.overlabel)
        self.over1 = ConnectedButton(self.cardsToGoOver, 0, self.ResumeBox, "over1")
        self.barreResume.addWidget(self.over1)
        self.over2 = ConnectedButton(self.cardsToGoOver, 1, self.ResumeBox, "over2")
        self.barreResume.addWidget(self.over2)
        self.over3 = ConnectedButton(self.cardsToGoOver, 2, self.ResumeBox, "over3")
        self.barreResume.addWidget(self.over3)
        # label cartes bien connues et les 3 boutons carte associés
        self.knowledgelabel = QLabel(self.ResumeBox)
        self.knowledgelabel.setObjectName("knowledgelabel")
        self.knowledgelabel.setText("  Cards known")
        self.barreResume.addWidget(self.knowledgelabel)
        self.know1 = ConnectedButton(self.cardsKnown, 0, self.ResumeBox, "know1")
        self.barreResume.addWidget(self.know1)
        self.know2 = ConnectedButton(self.cardsKnown, 1, self.ResumeBox, "know2")
        self.barreResume.addWidget(self.know2)
        self.know3 = ConnectedButton(self.cardsKnown, 2, self.ResumeBox, "know3")
        self.barreResume.addWidget(self.know3)
        # une ligne de séparation horizontale
        self.line2 = QFrame(self.ResumeBox)
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setObjectName("separation line n2")
        self.barreResume.addWidget(self.line2)
        # le bouton d'aide
        self.helpButton = QPushButton(u"Help", self.ResumeBox)
        self.helpButton.setObjectName("helpButton")
        self.barreResume.addWidget(self.helpButton)
        self.helpButton.setEnabled(False)

        ## ecran central changeant
        # au moment de l'ouverture ecran d'accueil
        # plus tard interface de parcours de carte, de lecture de cartes,
        # de jeu et de parcours de jeu
        ### le layout central avec les onglets
        self.screenLayout = QWidget(self.Dialog)
        self.screenLayout.setGeometry(QtCore.QRect(230, 60, 671, 501))
        self.screenLayout.setObjectName("screenLayout")
        self.myscreen=HomeScreen(self.screenLayout)

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
        self.myscreen.dragAndDropSignal.connect(self.openDragAndDrop)

    def getCards(self):
        self.cardsToLearn=database.getCardsToLearn(self.Table,0,4)
        self.cardsToGoOver=database.getCardsToLearn(self.Table,5,9)
        self.cardsKnown=database.getCardsToLearn(self.Table,10,10)
    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def retourAccueil(self):
        self.currentScreen.close()
        self.displayHomeScreen()
    def createnew(self):
        # ouverture de l'interface de creation
        self.createInterf = createcardsInterf.CardCreation(self.screenLayout)
        self.myscreen.setVisible(False)
        self.currentScreen = self.createInterf
        self.createInterf.show()
        self.createInterf.created.connect(self.displayHomeScreen)
    def modifycard(self):
        # la carte pour l'instant random
        self.selectedcard=database.getCardById("anglais", database.getRandomCard("anglais"))
        # ouverture de l'interface de modification
        self.modifInterf=createcardsInterf.CardModification(self.screenLayout, self.selectedcard)
        #on cache l'ecran d'accueil
        self.myscreen.setVisible(False)
        self.currentScreen = self.modifInterf
        self.modifInterf.show()
        self.modifInterf.modified.connect(self.displayHomeScreen)
        self.modifInterf.deleted.connect(self.displayHomeScreen)
    def openDragAndDrop(self):
        self.myscreen.setVisible(False)
        self.DDInterf = dragAndDrop.dragDropGame(self.screenLayout, database.getCardsToLearn('anglais',0,10))
        self.DDInterf.show()
        self.DDInterf.leave.connect(self.displayHomeScreen)
    def displayHomeScreen(self):
        self.getCards()
        self.myscreen.setVisible(True)
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
