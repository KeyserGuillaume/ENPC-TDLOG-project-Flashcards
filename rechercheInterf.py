############# definition de l'interface de recherche

import rechercheFonct
CondtPara = ["Mot", "Langue", "Traduction", "Phrase"]
EtOuPara = ["Et", "Ou"]

#from PyQt4.QtGui import QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox, QFileDialog
#from PyQt4 import QtCore

from PyQt5 import QtCore, QtWidgets 
from PyQt5.QtWidgets import QTextBrowser, QApplication, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QProgressBar, QSlider, QComboBox, QFileDialog

import sys

class Recherche(object):
    def __init__(self):
        ## La fenetre
        self.rechercheDialog=QWidget()
        self.rechercheDialog.setObjectName("Recherche")
        self.rechercheDialog.setFixedSize(979, 681)
        ## Textbrower pour afficher les resultats de recherche
        self.textbrowserResultat = QtWidgets.QTextBrowser(self.rechercheDialog)
        self.textbrowserResultat.setGeometry(QtCore.QRect(20, 190, 941, 471))
        self.textbrowserResultat.setObjectName("textbrowserResultat")        
        ## Layout au milieu
        self.milieuWidget = QtWidgets.QWidget(self.rechercheDialog)
        self.milieuWidget.setGeometry(QtCore.QRect(280, 130, 674, 42))
        self.milieuWidget.setObjectName("milieuWidget")
        self.mBoxlayout = QtWidgets.QHBoxLayout(self.milieuWidget)
        self.mBoxlayout.setContentsMargins(0, 0, 0, 0)
        self.mBoxlayout.setObjectName("mBoxlayout")
        ## Checkbox pour decider la recherche floue ou pas 
        self.chkFloue = QtWidgets.QCheckBox(u"Recherche floue", self.milieuWidget)
        self.chkFloue.setObjectName("chkFloue")
        self.chkFloue.setEnabled(False)
        self.mBoxlayout.addWidget(self.chkFloue)
        ## Button pour lancer la recherche
        self.btnLancer = QtWidgets.QPushButton(u"Lancer la recherche", self.milieuWidget)
        self.btnLancer.setObjectName("btnLancer")
        self.btnLancer.clicked.connect(self.lancer_recherche)
        self.mBoxlayout.addWidget(self.btnLancer)
        ## Button pour effacer les champs de recherche
        self.btnEffacer = QtWidgets.QPushButton(u"Effacer la recherche", self.milieuWidget)
        self.btnEffacer.setObjectName("btnEffacer")
        self.btnEffacer.setEnabled(False)
        self.btnEffacer.clicked.connect(self.click_btnEffacer) 
        self.mBoxlayout.addWidget(self.btnEffacer)
        ## Layout en haut, c'est un Gridlayout
        self.hautWidget = QtWidgets.QWidget(self.rechercheDialog)
        self.hautWidget.setGeometry(QtCore.QRect(15, 20, 941, 91))
        self.hautWidget.setObjectName("hautWidget")
        self.hGridlayout = QtWidgets.QGridLayout(self.hautWidget)
        self.hGridlayout.setContentsMargins(0, 0, 0, 0)
        self.hGridlayout.setObjectName("hGridlayout")
        ## L'un des sous-layouts en haut 
        self.hBoxlayout1 = QtWidgets.QHBoxLayout()
        self.hBoxlayout1.setObjectName("hBoxlayout1")
        ## ComboBox1 pour choisir un condition de recherche: Mot, Langue, Traduction, Phrase; Mot par defaut
        self.cmbCondt1 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbCondt1.setObjectName("cmbCondt1")
        self.cmbCondt1.addItems(CondtPara)
        self.cmbCondt1.setCurrentIndex(0)
        self.cmbCondt1.activated.connect(self.active_cmbCondt1)
        self.hBoxlayout1.addWidget(self.cmbCondt1)
        ## LineEdit1 pour recu l'input de ComboBox1
        self.leditCondtV1 = QtWidgets.QLineEdit(self.hautWidget)
        self.leditCondtV1.setObjectName("leditCondtV1")
        self.leditCondtV1.textEdited.connect(self.active_cmbCondt1)
        self.hBoxlayout1.addWidget(self.leditCondtV1)
        ## ComboBoxEtOu1 pour choisir 'Et' et 'Ou'
        self.cmbEtOu1 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbEtOu1.setObjectName("cmbEtOu1")
        self.cmbEtOu1.addItems(EtOuPara)
        self.cmbEtOu1.setCurrentIndex(0)
        self.cmbEtOu1.setEnabled(False)
        self.cmbEtOu1.activated.connect(self.active_cmbCondt2)
        self.hBoxlayout1.addWidget(self.cmbEtOu1)
        ## ComboBox2 pour choisir un condition de recherche: Mot, Langue, Traduction, Phrase; Langue par defaut
        self.cmbCondt2 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbCondt2.setObjectName("cmbCondt2")
        self.cmbCondt2.addItems(CondtPara)
        self.cmbCondt2.setCurrentIndex(1)
        self.cmbCondt2.setEnabled(False)
        self.cmbCondt2.activated.connect(self.active_cmbCondt2)
        self.hBoxlayout1.addWidget(self.cmbCondt2)
        ## LineEdit2 pour recu l'input de ComboBox2
        self.leditCondtV2 = QtWidgets.QLineEdit(self.hautWidget)
        self.leditCondtV2.setObjectName("leditCondtV2")
        self.leditCondtV2.setEnabled(False)
        self.leditCondtV2.textEdited.connect(self.active_cmbCondt2)
        self.hBoxlayout1.addWidget(self.leditCondtV2)
        self.hGridlayout.addLayout(self.hBoxlayout1, 1, 1, 1, 1)
        ## L'autre des sous-layouts en haut 
        self.hBoxlayout2 = QtWidgets.QHBoxLayout()
        self.hBoxlayout2.setObjectName("hBoxlayout2")
        ## ComboBox3 pour choisir un condition de recherche: Mot, Langue, Traduction, Phrase; Traduction par defaut
        self.cmbCondt3 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbCondt3.setObjectName("cmbCondt3")
        self.cmbCondt3.addItems(CondtPara)
        self.cmbCondt3.setCurrentIndex(2)
        self.cmbCondt3.setEnabled(False)
        self.cmbCondt3.activated.connect(self.active_cmbCondt3)
        self.hBoxlayout2.addWidget(self.cmbCondt3)
        ## LineEdit3 pour recu l'input de ComboBox3
        self.leditCondtV3 = QtWidgets.QLineEdit(self.hautWidget)
        self.leditCondtV3.setObjectName("leditCondtV3")
        self.leditCondtV3.setEnabled(False)
        self.leditCondtV3.textEdited.connect(self.active_cmbCondt3)
        self.hBoxlayout2.addWidget(self.leditCondtV3)
        ## ComboBoxEtOu3 pour choisir 'Et' et 'Ou'
        self.cmbEtOu3 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbEtOu3.setObjectName("cmbEtOu3")
        self.cmbEtOu3.addItems(EtOuPara)
        self.cmbEtOu3.setEnabled(False)
        self.hBoxlayout2.addWidget(self.cmbEtOu3)
        ## ComboBox4 pour choisir un condition de recherche: Mot, Langue, Traduction, Phrase; Phrase par defaut
        self.cmbCondt4 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbCondt4.setObjectName("cmbCondt4")
        self.cmbCondt4.addItems(CondtPara)
        self.cmbCondt4.setCurrentIndex(3)
        self.cmbCondt4.setEnabled(False)
        self.hBoxlayout2.addWidget(self.cmbCondt4)
        ## LineEdit4 pour recu l'input de ComboBox4
        self.leditCondtV4 = QtWidgets.QLineEdit(self.hautWidget)
        self.leditCondtV4.setObjectName("leditCondtV4")
        self.leditCondtV4.setEnabled(False)
        self.hBoxlayout2.addWidget(self.leditCondtV4)
        self.hGridlayout.addLayout(self.hBoxlayout2, 2, 1, 1, 1)
        ## ComboBoxEtOu2 pour choisir 'Et' et 'Ou', Attention: il est dans le Gridlayout
        self.cmbEtOu2 = QtWidgets.QComboBox(self.hautWidget)
        self.cmbEtOu2.setObjectName("cmbEtOu2")
        self.cmbEtOu2.addItems(EtOuPara)
        self.cmbEtOu2.setEnabled(False)
        self.cmbEtOu2.activated.connect(self.active_cmbCondt3)
        self.hGridlayout.addWidget(self.cmbEtOu2, 2, 0, 1, 1)
    def show(self):
        # ouverture de la fenetre
        self.rechercheDialog.show()
    def click_btnEffacer(self):
        self.textbrowserResultat.clear()
        self.cmbEtOu1.setCurrentIndex(0)
        self.cmbEtOu1.setEnabled(False)
        self.cmbEtOu2.setCurrentIndex(0)
        self.cmbEtOu2.setEnabled(False)
        self.cmbEtOu3.setCurrentIndex(0)
        self.cmbEtOu3.setEnabled(False)
        self.chkFloue.setChecked(False)
        self.chkFloue.setEnabled(False)
        self.leditCondtV1.clear()
        self.leditCondtV2.clear()
        self.leditCondtV2.setEnabled(False)
        self.leditCondtV3.clear()
        self.leditCondtV3.setEnabled(False)
        self.leditCondtV4.clear()
        self.leditCondtV4.setEnabled(False)
        self.cmbCondt1.setCurrentIndex(0)
        self.cmbCondt2.setCurrentIndex(1)
        self.cmbCondt2.setEnabled(False)
        self.cmbCondt3.setCurrentIndex(2)
        self.cmbCondt3.setEnabled(False)
        self.cmbCondt4.setCurrentIndex(3)
        self.cmbCondt4.setEnabled(False)
        self.btnEffacer.setEnabled(False)
    def active_cmbCondt1(self):
        self.chkFloue.setEnabled(True)
        self.btnEffacer.setEnabled(True)
        self.cmbEtOu1.setEnabled(True)
        self.cmbCondt2.setEnabled(True)
        self.leditCondtV2.setEnabled(True)
    def active_cmbCondt2(self):
        self.cmbEtOu2.setEnabled(True)
        self.cmbCondt3.setEnabled(True)
        self.leditCondtV3.setEnabled(True)
    def active_cmbCondt3(self):
        self.cmbEtOu3.setEnabled(True)
        self.cmbCondt4.setEnabled(True)
        self.leditCondtV4.setEnabled(True)
    def quit(self):
        exit(0)
    def lancer_recherche(self):
        if self.chkFloue.isChecked:
            floue = True
        else:
            floue = False
        condt1 = str(self.cmbCondt1.currentText())
        condtV1 = str(self.leditCondtV1.text())
        etou1 = str(self.cmbEtOu1.currentText())
        condt2 = str(self.cmbCondt2.currentText())
        condtV2 = str(self.leditCondtV2.text())
        etou2 = str(self.cmbEtOu2.currentText())
        condt3 = str(self.cmbCondt3.currentText())
        condtV3 = str(self.leditCondtV3.text())
        etou3 = str(self.cmbEtOu3.currentText())
        condt4 = str(self.cmbCondt4.currentText())
        condtV4 = str(self.leditCondtV4.text())
        resultat = rechercheFonct.recherche(floue, condt1, condtV1, etou1, condt2, condtV2, etou2, condt3, condtV3, etou3, condt4, condtV4)
        if len(resultat) == 0:
            self.textbrowserResultat.append("Aucun document ne correspond aux termes de recherche spécifiés (). Vous pouvez essayer d'autres mots")
        else:
            self.textbrowserResultat.append('\n'.join(str(resultat[k]) for k in range(len(resultat))))

        
        
        
        

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
 


    
        
        
        
        
        
        
        
        
        
        