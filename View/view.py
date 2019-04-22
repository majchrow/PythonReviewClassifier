#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QPlainTextEdit, QDesktopWidget
from PyQt5.QtCore import QSize
from Model.model import Classifier

IMAGES_LAYOUTS_PATH = 'images/layouts/'


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(960, 500))
        self.setMaximumSize(QSize(960, 500))
        self.setWindowTitle("Review Classifier")
        self.Center()
        self.init_ui()

    def init_ui(self):
        pass

    def _center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class StartWindow(Window):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black")

    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        # title = QLabel("Classify your review", self)
        # title.setAlignment(QtCore.Qt.AlignCenter)
        # gridLayout.addWidget(title, 0, 0)

        additionalLayout = QGridLayout(self)

        additionalLayout.setRowStretch(0, 5)
        additionalLayout.setRowStretch(1, 5)
        additionalLayout.setRowStretch(2, 5)
        additionalLayout.setRowStretch(3, 5)
        additionalLayout.setRowStretch(4, 5)
        additionalLayout.setColumnStretch(0, 5)
        additionalLayout.setColumnStretch(1, 5)
        additionalLayout.setColumnStretch(2, 5)
        additionalLayout.setColumnStretch(3, 5)
        additionalLayout.setColumnStretch(4, 5)

        label = QLabel(self)
        pixmap = QPixmap(IMAGES_LAYOUTS_PATH + 'main.jpg')
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        gridLayout.addWidget(label, 2, 2)

        button = QPushButton('Start')
        button.setStyleSheet("background-color: white")
        # button.setGeometry(0, 0, 50, 50)
        button.clicked.connect(self.start)
        self.dialog = MenuWindow()
        additionalLayout.addWidget(button, 2, 2)
        gridLayout.addLayout(additionalLayout, 2, 2)

    def start(self):
        self.close()
        self.dialog.show()


class MenuWindow(Window):
    def __init__(self):
        super().__init__()
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

        button.setStyleSheet("background-color: rgb(141, 194, 210)")
        button1.setStyleSheet("background-color: rgb(141, 194, 210)")
        button2.setStyleSheet("background-color: rgb(141, 194, 210)")

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

        # additionalLayout = QGridLayout(self)

        '''additionalLayout.setRowStretch(0, 5)
        additionalLayout.setRowStretch(1, 5)
        additionalLayout.setRowStretch(2, 5)
        additionalLayout.setRowStretch(3, 5)
        additionalLayout.setRowStretch(4, 5)

        additionalLayout.setColumnStretch(0, 5)
        additionalLayout.setColumnStretch(1, 5)
        additionalLayout.setColumnStretch(2, 5)
        additionalLayout.setColumnStretch(3, 5)
        additionalLayout.setColumnStretch(4, 5)

        additionalLayout.addWidget(button, 2, 2)

        gridLayout.addLayout(additionalLayout, 2, 1)'''

        label = QLabel(self)
        label.setPixmap(QPixmap(IMAGES_LAYOUTS_PATH + 'network.jpeg'))
        label1 = QLabel(self)
        label1.setPixmap(QPixmap(IMAGES_LAYOUTS_PATH + 'film.jpg'))
        label2 = QLabel(self)
        label2.setPixmap(QPixmap(IMAGES_LAYOUTS_PATH + 'text.png'))
        # .scaled(400, 500, QtCore.Qt.KeepAspectRatio))
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


class ChooseWindow(Window):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.init_ui()

    def init_ui(self):
        pass


class GenerateWindow(Window):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(141, 194, 210)")
        self.init_ui()

    def init_ui(self):
        pass


class ClassifyWindow(Window):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(141, 194, 210)")

    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        gridLayout.setRowStretch(0, 5)
        gridLayout.setColumnStretch(0, 5)
        gridLayout.setColumnStretch(1, 5)
        gridLayout.setColumnStretch(2, 5)

        text_area = QPlainTextEdit(self)
        text_area.setStyleSheet("background-color: white")
        text_area.insertPlainText("Write your review here.\n")

        button = QPushButton("Get back")
        button.setStyleSheet("background-color: white")
        button.clicked.connect(self.back)

        button2 = QPushButton("Classify")
        button2.setStyleSheet("background-color: white")
        button2.clicked.connect(self.classify)

        gridLayout.addWidget(text_area, 0, 0, 2, 2)
        # gridLayout.addWidget(button, 0, 1)

        additionalLayout = QGridLayout(self)

        additionalLayout.setRowStretch(0, 3)
        additionalLayout.setRowStretch(1, 3)
        additionalLayout.setRowStretch(2, 3)

        additionalLayout.setColumnStretch(0, 3)
        additionalLayout.setColumnStretch(1, 3)
        additionalLayout.setColumnStretch(2, 3)

        additionalLayout.addWidget(button, 1, 1)
        additionalLayout.addWidget(button2, 0, 1)

        gridLayout.addLayout(additionalLayout, 0, 2)

    def back(self):
        self.close()
        self.dialog_back = MenuWindow()
        self.dialog_back.show()

    def classify(self):
        self.dialog = MessageWindow()
        self.dialog.show()


class MessageWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(600, 200))
        self.setMaximumSize(QSize(600, 200))
        self.setWindowTitle("Message")
        self.setStyleSheet("background-color: white")
        self.init_ui()

    def init_ui(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        gridLayout.setRowStretch(0, 3)
        gridLayout.setRowStretch(1, 3)
        gridLayout.setRowStretch(2, 3)

        gridLayout.setColumnStretch(0, 3)
        gridLayout.setColumnStretch(1, 3)
        gridLayout.setColumnStretch(2, 3)

        label = QLabel(self)
        label.setFont(QFont("Arial", 12, QFont.Black))
        clf = Classifier() # this needs to be moved to controller, with all the view things
        clf.clf = "clf.pkl"
        prediction, proba = clf.predict("The best movie I've ever seen!")
        label.setText(f"Your review was classified as {prediction} with probability {proba:1.3f}%.")

        gridLayout.addWidget(label, 1, 1)
