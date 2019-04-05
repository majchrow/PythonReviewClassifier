#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QSize


class ViewWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1000, 1000))
        self.setWindowTitle("Review Classifier")
        self.setStyleSheet("background-color: black")

        self.init_ui()


    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        #title = QLabel("Classify your review", self)
        #title.setAlignment(QtCore.Qt.AlignCenter)
        #gridLayout.addWidget(title, 0, 0)

        gridLayout.setRowStretch(0,5)
        gridLayout.setRowStretch(1, 5)
        gridLayout.setRowStretch(2, 5)
        gridLayout.setRowStretch(3, 5)
        gridLayout.setRowStretch(4, 5)
        gridLayout.setColumnStretch(0, 5)
        gridLayout.setColumnStretch(1, 5)
        gridLayout.setColumnStretch(2, 5)
        gridLayout.setColumnStretch(3, 5)
        gridLayout.setColumnStretch(4, 5)

        label = QLabel(self)
        pixmap = QPixmap('main.jpg')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        gridLayout.addWidget(label, 2, 2)

        button = QPushButton('Start')
        button.setStyleSheet("background-color: white")
        #button.setGeometry(0, 0, 50, 50)
        button.clicked.connect(self.start)
        self.dialog = MenuWindow()
        gridLayout.addWidget(button, 2, 2)


    def start(self):
        self.close()
        self.dialog.show()



class MenuWindow(ViewWindow):
    def __init__(self):
        ViewWindow.__init__(self)
        self.setStyleSheet("background-color: white")
        self.dialog_choose = ChooseWindow()
        self.dialog_generate = GenerateWindow()
        self.dialog_classify = ClassifyWindow()

    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)


        button = QPushButton('Choose model')
        button1 = QPushButton('Classify your review')
        button2 = QPushButton('Generate text')

        button.setStyleSheet("background-color: red")
        button1.setStyleSheet("background-color: rgb(141, 194, 210)")
        button2.setStyleSheet("background-color: green")

        button.clicked.connect(self.choose)
        button1.clicked.connect(self.classify)
        button2.clicked.connect(self.generate)

        gridLayout.setRowStretch(0, 5)
        gridLayout.setRowStretch(1, 5)
        gridLayout.setRowStretch(2, 5)
        gridLayout.setRowStretch(3, 5)
        gridLayout.setRowStretch(4, 5)
        gridLayout.setColumnStretch(0, 5)
        gridLayout.setColumnStretch(1, 5)
        gridLayout.setColumnStretch(2, 5)
        gridLayout.setColumnStretch(3, 5)
        gridLayout.setColumnStretch(4, 5)

        gridLayout.addWidget(button, 2, 1)
        gridLayout.addWidget(button1, 2, 2)
        gridLayout.addWidget(button2, 2, 3)

        label = QLabel(self)
        label.setPixmap(QPixmap('network.jpeg'))
        label1 = QLabel(self)
        label1.setPixmap(QPixmap('film.jpg'))
        label2 = QLabel(self)
        label2.setPixmap(QPixmap('text.png'))
        #.scaled(400, 500, QtCore.Qt.KeepAspectRatio))
        gridLayout.addWidget(label, 1, 1)
        gridLayout.addWidget(label1, 1, 2)
        gridLayout.addWidget(label2, 1, 3)

    def choose(self):
        self.close()
        self.dialog_choose.show()

    def generate(self):
        self.close()
        self.dialog_generate.show()

    def classify(self):
        self.close()
        self.dialog_classify.show()

class ChooseWindow(ViewWindow):
    def __init__(self):
        ViewWindow.__init__(self)
        self.setStyleSheet("background-color: white")

    def init_ui(self):
        pass


class GenerateWindow(ViewWindow):
    def __init__(self):
        ViewWindow.__init__(self)
        self.setStyleSheet("background-color: white")

    def init_ui(self):
        pass

class ClassifyWindow(ViewWindow):
    def __init__(self):
        ViewWindow.__init__(self)
        self.setStyleSheet("background-color: rgb(141, 194, 210)")

    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        gridLayout.setRowStretch(0, 5)
        gridLayout.setColumnStretch(0, 5)
        gridLayout.setColumnStretch(1, 5)

        text_area = QPlainTextEdit(self)
        text_area.setStyleSheet("background-color: white")
        text_area.insertPlainText("You can write text here.\n")

        button = QPushButton("Get back")
        button.setStyleSheet("background-color: white")
        button.clicked.connect(self.start)

        gridLayout.addWidget(text_area, 0, 0)
        gridLayout.addWidget(button, 0, 1)

    def start(self):
        self.close()
        self.dialog_back = MenuWindow()
        self.dialog_back.show()
