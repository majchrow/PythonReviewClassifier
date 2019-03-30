#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets
from src.view import ViewWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ViewWindow()
    mainWin.show()
    sys.exit( app.exec_() )