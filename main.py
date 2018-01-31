from PyQt5.QtWidgets import QApplication
from view import interfaccueil
import sys

if __name__ == "__main__":
    args = sys.argv
    a = QApplication(args)
    mf = interfaccueil.WelcomeInterf()
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)
    # sys.exit(a.exec_())
