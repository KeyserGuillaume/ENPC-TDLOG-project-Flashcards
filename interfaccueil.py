#interface global à afficher à l'ouverture

### contenus de carte à aller recuperer dans la database : comment ?
# sur le niveau de maitrise ?
## les listes suivantes doivent OBLIGATOIREMENT contenir au moins 2 items (len>1)
## dans le cas contraire on les complète par "..."
cardsToLearn=["suspendre","remuer","..."] # entre 0 et 4
cardsToGoOver=["echarpe","amour", "..."]  # entre 5 et 9
cardsKnown=["bonjour","bienvenue", "..."] # 10

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QGroupBox, QVBoxLayout, QCommandLinkButton, QLabel, QFrame, QToolBox
import sys

import createcardsInterf, database, flashcard, rechercheInterf, parcours

class HomeScreen(object):
    def __init__(self, givenLayout):
        # la boite a onglets
        self.mainpage = QVBoxLayout(givenLayout)
        self.mainpage.setContentsMargins(0, 0, 0, 0)
        self.mainpage.setObjectName("mainpage")
        self.ongletsAccueil = QToolBox(givenLayout)
        self.ongletsAccueil.setObjectName("ongletsAccueil")
        # onglet 1
        self.MesCartes = QWidget()
        self.MesCartes.setGeometry(QtCore.QRect(0, 0, 689, 431))
        self.MesCartes.setObjectName("MesCartes")
        folders = parcours.parcoursLanguesFolder( self.MesCartes)
        self.ongletsAccueil.addItem(self.MesCartes, "")
        self.ongletsAccueil.setItemText(self.ongletsAccueil.indexOf(self.MesCartes),"Mes Cartes")
        # onglet 2
        self.MesJeux = QWidget()
        self.MesJeux.setGeometry(QtCore.QRect(0, 0, 669, 431))
        self.MesJeux.setObjectName("MesJeux")
        iconesJeux = parcours.parcoursIconsGame(self.MesJeux)
        self.ongletsAccueil.addItem(self.MesJeux, "")
        self.ongletsAccueil.setItemText(self.ongletsAccueil.indexOf(self.MesJeux), "Mes Jeux")
        self.mainpage.addWidget(self.ongletsAccueil)
        # onglet 3
        self.MesParties = QWidget()
        self.MesParties.setGeometry(QtCore.QRect(0, 0, 649, 431))
        self.MesParties.setObjectName("MesParties")
        self.ongletsAccueil.addItem(self.MesParties, "")
        self.ongletsAccueil.setItemText(self.ongletsAccueil.indexOf(self.MesParties), "Mes Parties")
        self.mainpage.addWidget(self.ongletsAccueil)
        # selection de l'onglet principal
        self.ongletsAccueil.setCurrentIndex(0)


class WelcomeInterf(object):
    def __init__(self):
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
        self.accueil.setEnabled(False)
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
        self.learn1 = QCommandLinkButton(self.ResumeBox)
        self.learn1.setObjectName("learn1")
        self.learn1.setText(cardsToLearn[0])
        self.barreResume.addWidget(self.learn1)
        self.learn2 = QCommandLinkButton(self.ResumeBox)
        self.learn2.setObjectName("learn2")
        self.learn2.setText(cardsToLearn[1])
        self.barreResume.addWidget(self.learn2)
        self.learn3 = QCommandLinkButton(self.ResumeBox)
        self.learn3.setObjectName("learn3")
        self.learn3.setText("...")
        self.barreResume.addWidget(self.learn3)
        # label cartes a revoir et les 3 boutons carte associés
        self.overlabel = QLabel(self.ResumeBox)
        self.overlabel.setObjectName("overlabel")
        self.overlabel.setText("  Cards to go over")
        self.barreResume.addWidget(self.overlabel)
        self.over1 = QCommandLinkButton(self.ResumeBox)
        self.over1.setObjectName("over1")
        self.over1.setText(cardsToGoOver[0])
        self.barreResume.addWidget(self.over1)
        self.over2 = QCommandLinkButton(self.ResumeBox)
        self.over2.setObjectName("over2")
        self.over2.setText(cardsToGoOver[1])
        self.barreResume.addWidget(self.over2)
        self.over3 = QtWidgets.QCommandLinkButton(self.ResumeBox)
        self.over3.setObjectName("over3")
        self.over3.setText("...")
        self.barreResume.addWidget(self.over3)
        # label cartes bien connues et les 3 boutons carte associés
        self.knowledgelabel = QLabel(self.ResumeBox)
        self.knowledgelabel.setObjectName("knowledgelabel")
        self.knowledgelabel.setText("  Cards known")
        self.barreResume.addWidget(self.knowledgelabel)
        self.know1 = QCommandLinkButton(self.ResumeBox)
        self.know1.setObjectName("know1")
        self.know1.setText(cardsKnown[0])
        self.barreResume.addWidget(self.know1)
        self.know2 = QCommandLinkButton(self.ResumeBox)
        self.know2.setObjectName("know2")
        self.know2.setText(cardsKnown[1])
        self.barreResume.addWidget(self.know2)
        self.know3 = QCommandLinkButton(self.ResumeBox)
        self.know3.setObjectName("know3")
        self.know3.setText("...")
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
        self.selectedcard=None
        self.modifInterf=None
        self.modifyButton.clicked.connect(self.modifycard)
        self.searchInterf = None
        self.searchButton.clicked.connect(self.search)

    def show(self):
        # ouverture de la fenetre
        self.Dialog.show()
    def createnew(self):
        # ouverture de linterface de creation
        self.createInterf = createcardsInterf.CardCreation()
        self.createInterf.show()
    def modifycard(self):
        # la carte pour l'instant random
        self.selectedcard=database.getCardById("anglais", database.getRandomCard("anglais"))
        # ouverture de linterface de modification
        self.modifInterf=createcardsInterf.CardModification(self.selectedcard)
        self.modifInterf.show()
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
