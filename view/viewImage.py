from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout, QShortcut, QLabel, QLineEdit
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from model import imageAPI

from view.icons import icons
# permet l'acces aux images des icones

class ViewImageWindow(QWidget):
    def __init__(self, parentWindow, word, previousDisplay):
        self.word = word
        self.nextDisplay = previousDisplay
        self.parentWindow = parentWindow
        self.chosenImagePath = ""
        self.provider = imageAPI.ImageProvider(self.word)
        self.paths = list()
        self.pixmaps = list()
        self.currentIndex = 0
    def stealTheLimelight(self):
        self.background = QWidget(self.parentWindow)
        self.background.resize(self.parentWindow.frameSize())
        self.background.setStyleSheet("background-color: rgba(10, 10, 10, 0.8);\n")
        self.background.show()
        super(ViewImageWindow, self).__init__(self.parentWindow)
        self.resize(self.parentWindow.frameSize())
        VLayout = QVBoxLayout(self)
        self.viewWidget = QLabel(self)
        self.viewWidget.setAlignment(QtCore.Qt.AlignCenter)
        self.viewWidget.resize(self.frameSize().width(), self.frameSize().height()-80)
        self.fillUpPixmaps()
        if len(self.pixmaps) > 0:
            self.viewWidget.setPixmap(self.pixmaps[0])
        VLayout.addWidget(self.viewWidget)
        bottomWidget = QWidget(self)
        bottomWidget.setFixedSize(500, 80)
#        bottomWidget.setMaximumSize(500, 100)
        bottomHLayout = QHBoxLayout(bottomWidget)
        self.leftButton = QPushButton("previous", bottomWidget)
        self.leftButton.setEnabled(False)
        bottomHLayout.addWidget(self.leftButton)
        decisionWidget = QWidget(bottomWidget)
        gridLayout = QGridLayout(decisionWidget)
        self.cancelButton = QPushButton("Cancel", decisionWidget)
        gridLayout.addWidget(self.cancelButton, 0, 0, 1, 1)
        self.chooseButton = QPushButton("Choose This Picture", decisionWidget)
        gridLayout.addWidget(self.chooseButton, 0, 1, 1, 1)
        label = QLabel("Change Search Field", decisionWidget)
        label.setStyleSheet("color: rgba(255, 255, 255);")
        gridLayout.addWidget(label, 1, 0, 1, 1)
        self.searchField = QLineEdit(self.word.replace(' ', '+'), decisionWidget)
        gridLayout.addWidget(self.searchField)
        bottomHLayout.addWidget(decisionWidget)
        self.rightButton = QPushButton("next", bottomWidget)
        bottomHLayout.addWidget(self.rightButton)
        VLayout.addWidget(bottomWidget)
        VLayout.setAlignment(bottomWidget, QtCore.Qt.AlignCenter)
#        tmpbackground = QWidget(bottomWidget)
#        tmpbackground.resize(bottomWidget.frameSize())
#        tmpbackground.setStyleSheet("background-color: rgba(10, 10, 100, 0.7);\n")
        self.show()
        
        self.nextShortcut=QShortcut(QtGui.QKeySequence('Right'), self)
        self.prevShortcut=QShortcut(QtGui.QKeySequence('Left'), self)
        self.chooseShortcut=QShortcut(QtGui.QKeySequence('Enter'), self)
        self.nextShortcut.activated.connect(self.nextImage)
        self.prevShortcut.activated.connect(self.previousImage)
        self.chooseShortcut.activated.connect(self.choose)
        self.cancelButton.clicked.connect(self.cancel)
        self.leftButton.clicked.connect(self.previousImage)
        self.rightButton.clicked.connect(self.nextImage)
        self.searchField.editingFinished.connect(self.newSearch)
        self.chooseButton.clicked.connect(self.choose)
    redirect = QtCore.pyqtSignal()
    done = QtCore.pyqtSignal()
    
    def getPixmap(self, path):
        pixmap = QtGui.QPixmap()
        pixmap.load(path)
        pixmap = pixmap.scaled(self.viewWidget.frameSize().width(),
                                         self.viewWidget.frameSize().height()-30,
                                         QtCore.Qt.KeepAspectRatio)
        return pixmap
    
    def fillUpPixmaps(self):
        paths_batch = self.provider.getImageBatch()
        [self.pixmaps.append(self.getPixmap(path)) for path in paths_batch]
        self.paths += paths_batch
        
    def nextImage(self):
        self.currentIndex += 1
        if self.currentIndex == len(self.pixmaps):
            n = len(self.pixmaps)
            self.fillUpPixmaps()
            if len(self.pixmaps) == n:
                self.rightButton.setEnabled(False)
                self.nextShortcut.setEnabled(False)
                return
        self.viewWidget.setPixmap(self.pixmaps[self.currentIndex])
        if self.currentIndex == 1:
            self.leftButton.setEnabled(True)
            self.prevShortcut.setEnabled(True)
        
    def previousImage(self):
        if self.currentIndex == 0:
            return
        self.currentIndex -= 1
        self.viewWidget.setPixmap(self.pixmaps[self.currentIndex])
        if self.currentIndex == 0:
            self.leftButton.setEnabled(False)
            self.prevShortcut.setEnabled(False)
        if self.currentIndex == len(self.pixmaps)-1:
            self.rightButton.setEnabled(True)
            self.nextShortcut.setEnabled(True)
            self.previousImage()
    
    def newSearch(self):
        newWord = str(self.searchField.text())
        if newWord == self.word:
            return
        self.word = newWord
        self.provider = imageAPI.ImageProvider(self.word)
        self.pixmaps = list()
        self.paths = list()
        self.currentIndex = 0
        self.fillUpPixmaps()
        self.viewWidget.setPixmap(self.pixmaps[0])
        self.leftButton.setEnabled(False)
        self.prevShortcut.setEnabled(False)
        self.rightButton.setEnabled(True)
        self.nextShortcut.setEnabled(True)
        
    def choose(self):
        if len(self.paths)==0:
            return
        if self.currentIndex==len(self.paths):
            self.currentIndex -= 1
        self.chosenImagePath = self.provider.keepImage(self.paths[self.currentIndex])
        self.done.emit()
        
    def cancel(self):
        self.chosenImagePath = ""
        self.done.emit()
        
    def toTheShadows(self):
        self.provider.cleanUp()
        self.background.close()
        self.close()
        
if __name__=="__main__":
    args = sys.argv
    a = QApplication(args)
    w = QWidget()
    w.resize(670, 500)
    v = ViewImageWindow(w, "witch", None)
    w.show()
    v.stealTheLimelight()
    v.done.connect(v.toTheShadows)
    a.exec_()
    a.lastWindowClosed.connect(a.quit)