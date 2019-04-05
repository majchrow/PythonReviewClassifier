#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from src.view import ViewWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = ViewWindow()
    mainWin.show()
    sys.exit( app.exec_() )