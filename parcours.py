from PyQt5 import QtCore, QtGui, QtWidgets

_root = QtCore.QFileInfo(__file__).absolutePath()

from icons import icons

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(663, 406)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(101, 91))
        self.pushButton.setMaximumSize(QtCore.QSize(101, 91))
        self.pushButton.setStyleSheet("background-image: url(:/icons/dossier.png);\n"
"font: 75 14pt \"Arial\";")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(101, 101))
        self.pushButton_4.setMaximumSize(QtCore.QSize(101, 101))
        self.pushButton_4.setStyleSheet("background-image: url(:/icons/dragdrop.png);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 2, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(101, 91))
        self.pushButton_6.setMaximumSize(QtCore.QSize(101, 91))
        self.pushButton_6.setStyleSheet("background-image: url(:/icons/dossier.png);\n"
"font: 75 14pt \"Arial\";")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(101, 91))
        self.pushButton_7.setMaximumSize(QtCore.QSize(101, 91))
        self.pushButton_7.setStyleSheet("background-image: url(:/icons/dossier.png);\n"
"font: 75 14pt \"Arial\";")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(101, 101))
        self.pushButton_2.setMaximumSize(QtCore.QSize(101, 101))
        self.pushButton_2.setStyleSheet("background-image: url(:/icons/memory.png);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(101, 101))
        self.pushButton_3.setMaximumSize(QtCore.QSize(101, 101))
        self.pushButton_3.setStyleSheet("background-image: url(:/icons/hotcold.png);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(131, 101))
        self.pushButton_5.setMaximumSize(QtCore.QSize(131, 101))
        self.pushButton_5.setStyleSheet("background-image: url(:/icons/pointTo.png);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 3, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(101, 91))
        self.pushButton_8.setMaximumSize(QtCore.QSize(101, 91))
        self.pushButton_8.setStyleSheet("background-image: url(:/icons/dossier.png);\n"
"font: 75 14pt \"Arial\";")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Anglais"))
        self.pushButton_4.setText(_translate("Dialog", " "))
        self.pushButton_6.setText(_translate("Dialog", "Espagnol"))
        self.pushButton_7.setText(_translate("Dialog", "Autres"))
        self.pushButton_2.setText(_translate("Dialog", " "))
        self.pushButton_3.setText(_translate("Dialog", " "))
        self.pushButton_5.setText(_translate("Dialog", " "))
        self.pushButton_8.setText(_translate("Dialog", "Francais"))

import sys

def main():
    args = sys.argv
    a = QtWidgets.QApplication(args)
    MyDialog=QtWidgets.QWidget()
    mf = Ui_Dialog()
    mf.setupUi(MyDialog)
    MyDialog.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)

if __name__ == "__main__":
    main()
