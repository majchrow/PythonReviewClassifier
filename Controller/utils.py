#!/usr/bin/env python3

import sys
import Model.loader
import View.view
from Model.model import Classifier, LanguageModel
from View.view import StartWindow, MenuWindow, ChooseWindow, GenerateWindow, ClassifyWindow, MessageWindow
from PyQt5.QtWidgets import QApplication


class Start:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._view = StartWindow(self)
        self.dialog = MenuController()

    def run(self):
        self._view.show()
        return self._app.exec_()

    def on_click_start(self):
        self._view.close()
        self.dialog.run()


class MenuController:
    def __init__(self):
        self._view = MenuWindow(self)
        self.dialog_trainer = TrainerController()
        self.dialog_language = LanguageController()
        self.dialog_classifier = ClassifierController()

    def run(self):
        self._view.show()

    def on_click_choose(self):
        self._view.close()
        self.dialog_trainer.run()

    def on_click_generate(self):
        self._view.close()
        self.dialog_language.run()

    def on_click_classify(self):
        self._view.close()
        self.dialog_classifier.run()


class TrainerController:
    def __init__(self):
        self._lm = LanguageModel()
        self._clf = Classifier()
        self._view = ChooseWindow(self)

    def run(self):
        self._view.show()

    def get_lm(self):
        return Model.loader.get_lm()

    def get_cm(self):
        return Model.loader.get_clf()

    def on_click_item_cm(self):
        item = self._view.list_widget_cm.currentItem()
        self._clf.clf = item.text()
        self._view.current_cm_model.setText(self._clf.clf_name)

    def on_click_item_lm(self):
        item = self._view.list_widget_lm.currentItem()
        self._lm.lm = item.text()
        self._view.current_lm_model.setText(self._lm.lm_name)

    def on_click_back(self):
        self.dialog_back = MenuController()
        self._view.close()
        self.dialog_back.run()


class LanguageController:
    def __init__(self):
        self._lm = LanguageModel()
        self._view = GenerateWindow(self)

    def run(self):
        self._view.show()


class ClassifierController:
    def __init__(self):
        self._view = ClassifyWindow(self)
        self._clf = Classifier()
        self.dialog_message = MessageController()

    def run(self):
        self._view.show()

    def get_current_model(self):
        return Classifier().clf_name

    def on_click_classify(self):
        review = str(self._view.text_area.toPlainText())
        self._clf.clf = "clf.pkl"
        prediction, proba = self._clf.predict(review)
        self.dialog_message.__setattr__("prediction", prediction)
        self.dialog_message.__setattr__("proba", proba)
        self.dialog_message.run()

    def on_click_back(self):
        self.dialog_back = MenuController()
        self._view.close()
        self.dialog_back.run()


class MessageController:
    def __init__(self):
        self._view = MessageWindow(self)
        self.prediction = ""
        self.proba = 0.0

    def run(self):
        self._view.label.setText(f"Your review was classified as {self.prediction} with probability {self.proba:1.3f}%.")
        self._view.show()
