#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from src.view import StartWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = StartWindow()
    mainWin.show()
    sys.exit( app.exec_() )