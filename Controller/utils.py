#!/usr/bin/env python3

import sys
from Model.model import Classifier, LanguageModel
from View.view import StartWindow, MenuWindow, ChooseWindow, GenerateWindow, ClassifyWindow
from PyQt5.QtWidgets import QApplication


class Start:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._view = StartWindow()

    def run(self):
        self._view.show()
        return self._app.exec_()


class MenuController:
    def __init__(self):
        self._view = MenuWindow()


class TrainerController:
    def __init__(self):
        self._lm = LanguageModel()
        self._clf = Classifier()
        self._view = ChooseWindow()


class LanguageController:
    def __init__(self):
        self._lm = LanguageModel()
        self._view = GenerateWindow()


class ClassifierController:
    def __init__(self):
        self._clf = Classifier()
        self._view = ClassifyWindow()
