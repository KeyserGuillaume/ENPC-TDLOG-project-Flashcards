############# definition de l'interface de recherche

import rechercheFonct, database, flashcard

#from PyQt4.QtGui import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox, QFileDialog
#from PyQt4 import QtCore

langues = database.giveAllLanguages()
langues.insert(0, 'TOUTES')

from PyQt5 import QtCore, QtWidgets 
from PyQt5.QtWidgets import QTextBrowser, QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox, QFileDialog

import sys

class Recherche(object):
    def __init__(self):
        ## La fenetre
        self.rechercheDialog=QWidget()
        self.rechercheDialog.setObjectName("Recherche")
        self.rechercheDialog.setFixedSize(894, 593)
        ## Layout en haut
        self.hautWidget = QtWidgets.QWidget(self.rechercheDialog)
        self.hautWidget.setGeometry(QtCore.QRect(30, 10, 841, 51))
        self.hautWidget.setObjectName("hautWidget")
        self.hautLayout = QtWidgets.QHBoxLayout(self.hautWidget)
        self.hautLayout.setContentsMargins(0, 0, 0, 0)
        self.hautLayout.setObjectName("hautLayout")
        ## Recherche d'apres Langue 
        self.lb_langue = QtWidgets.QLabel(u"Langue:", self.hautWidget)
        self.lb_langue.setObjectName("lb_langue")
        self.hautLayout.addWidget(self.lb_langue)
        self.comboB_langue = QtWidgets.QComboBox(self.hautWidget)
        self.comboB_langue.setObjectName("comboB_langue")
        self.comboB_langue.addItems(langues)
        self.comboB_langue.activated.connect(self.active_text)
        self.hautLayout.addWidget(self.comboB_langue)
        ## Recherche d'apres Mot
        self.lb_mot = QtWidgets.QLabel(u"Mot:", self.hautWidget)
        self.lb_mot.setObjectName("lb_mot")
        self.hautLayout.addWidget(self.lb_mot)
        self.lineE_mot = QtWidgets.QLineEdit(self.hautWidget)
        self.lineE_mot.setObjectName("lineE_mot")
        self.lineE_mot.textEdited.connect(self.active_text)
        self.hautLayout.addWidget(self.lineE_mot)
        ## Recherche d'apres Theme
        self.lb_theme = QtWidgets.QLabel(u"Thème:", self.hautWidget)
        self.lb_theme.setObjectName("lb_theme")
        self.hautLayout.addWidget(self.lb_theme)
        self.lineE_theme = QtWidgets.QLineEdit(self.hautWidget)
        self.lineE_theme.setObjectName("lineE_theme")
        self.lineE_theme.textEdited.connect(self.active_text)
        self.hautLayout.addWidget(self.lineE_theme)        
        ## Layout au milieu
        self.milieuWidget = QtWidgets.QWidget(self.rechercheDialog)
        self.milieuWidget.setGeometry(QtCore.QRect(30, 70, 841, 41))
        self.milieuWidget.setObjectName("milieuWidget")
        self.milieuLayout = QtWidgets.QHBoxLayout(self.milieuWidget)
        self.milieuLayout.setContentsMargins(0, 0, 0, 0)
        self.milieuLayout.setObjectName("milieuLayout")
        ## Recherche d'apres Traduction
        self.lb_tra = QtWidgets.QLabel(u"Traduction:", self.milieuWidget)
        self.lb_tra.setObjectName("lb_tra")
        self.milieuLayout.addWidget(self.lb_tra)
        self.lineE_tra = QtWidgets.QLineEdit(self.milieuWidget)
        self.lineE_tra.setObjectName("lineE_tra")
        self.lineE_tra.textEdited.connect(self.active_text)
        self.milieuLayout.addWidget(self.lineE_tra)
        ## Recherche d'apres Phrase
        self.lb_phrase = QtWidgets.QLabel(u"Phrase:", self.milieuWidget)
        self.lb_phrase.setObjectName("lb_phrase")
        self.milieuLayout.addWidget(self.lb_phrase)
        self.lineE_phrase = QtWidgets.QLineEdit(self.milieuWidget)
        self.lineE_phrase.setObjectName("lineE_phrase")
        self.lineE_phrase.textEdited.connect(self.active_text)
        self.milieuLayout.addWidget(self.lineE_phrase)
        ## Layout en bas
        self.basWidget = QtWidgets.QWidget(self.rechercheDialog)
        self.basWidget.setGeometry(QtCore.QRect(110, 142, 761, 42))
        self.basWidget.setObjectName("widget2")
        self.basLayout = QtWidgets.QHBoxLayout(self.basWidget)
        self.basLayout.setContentsMargins(0, 0, 0, 0)
        self.basLayout.setObjectName("basLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.basLayout.addItem(spacerItem)
        self.checkB_floue = QtWidgets.QCheckBox(u"Recherche floue", self.basWidget)
        self.checkB_floue.setObjectName("checkB_floue")
        self.basLayout.addWidget(self.checkB_floue)
        self.btn_lancer = QtWidgets.QPushButton(u"Lancer la recherche", self.basWidget)
        self.btn_lancer.setObjectName("btn_lancer")
        self.btn_lancer.clicked.connect(self.click_btn_lancer)
        self.basLayout.addWidget(self.btn_lancer)
        self.btn_effacer = QtWidgets.QPushButton(u"Effacer la recherche", self.basWidget)
        self.btn_effacer.setObjectName("btn_effacer")
        self.btn_effacer.setEnabled(False)
        self.btn_effacer.clicked.connect(self.click_btn_effacer)
        self.basLayout.addWidget(self.btn_effacer)        
        ## Textbrower pour afficher les resultats de recherche
        self.textBrowser_resultat = QtWidgets.QTextBrowser(self.rechercheDialog)
        self.textBrowser_resultat.setGeometry(QtCore.QRect(20, 200, 851, 371))
        self.textBrowser_resultat.setObjectName("textBrowser_resultat")   
    def show(self):
        # ouverture de la fenetre
        self.rechercheDialog.show()
    def active_text(self):
        self.btn_effacer.setEnabled(True)
    def click_btn_effacer(self):
        self.textBrowser_resultat.clear()
        self.comboB_langue.setCurrentIndex(0)
        self.lineE_mot.clear()
        self.lineE_theme.clear()
        self.lineE_tra.clear()
        self.lineE_phrase.clear()
        self.checkB_floue.setChecked(False)
        self.btn_effacer.setEnabled(False)
    def click_btn_lancer(self):
        self.textBrowser_resultat.clear()
        self.btn_effacer.setEnabled(True)
        result = rechercheFonct.recherche(str(self.comboB_langue.currentText()), str(self.lineE_mot.text()), str(self.lineE_theme.text()), str(self.lineE_tra.text()), str(self.lineE_phrase.text()), self.checkB_floue.isChecked())
        if len(result) == 0:
            self.textBrowser_resultat.append("Aucun document ne correspond aux termes de recherche spécifiés. Vous pouvez essayer d'autres mots")
        else:
            for item in result:
                self.textBrowser_resultat.append('ID: {}   MOT: {}   THEME: {} \nTRADUCTION: {} \nEXEMPLE: {} \n\n'.format(item.name, item.word, item.thema, item.trad, item.exemple))
    def close(self):
        self.rechercheDialog.close()   



if __name__ == "__main__":
    args=sys.argv
    a = QApplication(args)
    re = Recherche()
    re.show()
    # appliquer les regles souhaitees
    resultat = a.exec_()
    #a.exec_()
    a.lastWindowClosed.connect(a.quit)
    #mf.quit()
    #sys.exit(resultat)
 


    
        
        
        
        
        
        
        
        
        
        