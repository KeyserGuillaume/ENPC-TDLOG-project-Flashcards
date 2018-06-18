from PyQt5.QtWidgets import QApplication
from view import homeInterface
import sys

if __name__ == "__main__":
    args = sys.argv
    a = QApplication(args)
    mf = homeInterface.WelcomeInterf()
    mf.show()
    a.exec_()
    a.lastWindowClosed.connect(a.quit)
    # sys.exit(a.exec_())
