from model import database

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox
from view.editCardsInterf import pop_upWidget

class CardCreation(QWidget):
    def __init__(self, parent, previousDisplay, language):
        self.parent = parent
        self.nextDisplay = previousDisplay
        self.language = language

class eraseLanguageInterf(QWidget):
    """
    Give the possibility to erase a language not needed anymore. Asks for confirmation.
    """
    def __init__(self, parent):
        self.parent = parent
        self.nextDisplay = "home"
    def stealTheLimelight(self):
        super(eraseLanguageInterf, self).__init__(self.parent)
        self.resize(self.parent.frameSize())
        self.primaryLayout = QVBoxLayout(self)
        self.query = QLabel("Please choose the language you want to erase.", self)
        self.primaryLayout.addWidget(self.query)
        self.languageBox = QComboBox(self)
        languages = database.giveAllLanguages()
        for possibleLanguage in languages:
            self.languageBox.addItem(possibleLanguage)
        self.primaryLayout.addWidget(self.languageBox)
        self.secondaryLayout = QHBoxLayout(self)
        self.yesButton = QPushButton("erase language", self)
        self.secondaryLayout.addWidget(self.yesButton)
        self.noButton = QPushButton("cancel", self)
        self.secondaryLayout.addWidget(self.noButton)
        self.primaryLayout.addLayout(self.secondaryLayout)
        self.yesButton.clicked.connect(self.confirmDeletion)
        self.noButton.clicked.connect(self.redirect.emit)
        self.primaryLayout.addSpacing(3*self.parent.frameSize().height()//4)
        self.show()
    redirect=QtCore.pyqtSignal()
    def confirmDeletion(self):
        self.language = str(self.languageBox.currentText())
        deletionMessage = ("After deletion, all {} cards in '{}' will be forever lost. \n" + \
        "Are you sure you want to continue ?").format(database.countLanguage(self.language), self.language)
        self.pop_up = pop_upWidget(self.parent, deletionMessage, "Delete '{}'".format(self.language), "Cancel")
        self.pop_up.accept.connect(self.eraseLanguage)
        self.pop_up.refuse.connect(self.redirect.emit)
        self.setVisible(False)
        self.pop_up.show()
    def eraseLanguage(self):
        database.removeLanguage(self.language)
        self.redirect.emit()
    def toTheShadows(self):
        self.close()