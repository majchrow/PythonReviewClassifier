#!/usr/bin/env python3

import sys
import logging
import Model.loader as loader
from Model.classifier import Classifier
from Model.classifier_adapter import create_adapter
from Model.language import LanguageModel
from View.view import StartWindow, MenuWindow, ChooseWindow, GenerateWindow, ClassifyWindow, MessageWindow
from PyQt5.QtWidgets import QApplication


class Start:
    """Starting window controller"""
    def __init__(self):
        logging.info("Initializing starting window controller")
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
    """Choosing menu window controller"""
    def __init__(self):
        logging.info("Initializing choosing menu controller")
        self._view = MenuWindow(self)
        self.dialog_trainer = ModelSelectorController()
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


class ModelSelectorController:
    """Model selector window controller"""
    def __init__(self):
        logging.info("Initializing model selector controller")
        self._lm = LanguageModel()
        self._clf = Classifier()
        self._view = ChooseWindow(self)

    def run(self):
        self._view.show()

    @staticmethod
    def get_all_lm():
        return loader.get_all_lm()

    @staticmethod
    def get_all_clf():
        return loader.get_all_clf()

    def on_click_apply_clf(self):
        clf = self._view.combo_box_clf.currentText()
        self._clf.clf = create_adapter(clf)
        self._view.current_clf.setText(clf)

    def on_click_apply_lm(self):
        lm = self._view.combo_box_lm.currentText()
        self._lm.lm = lm
        self._view.current_lm.setText(self._lm.name)

    def on_click_back(self):
        self.dialog_back = MenuController()
        self._view.close()
        self.dialog_back.run()

    def get_current_lm(self):
        if self._lm is not None:
            return self._lm.name
        else:
            return ""

    def get_current_clf(self):
        if self._clf is not None:
            return self._clf.name
        else:
            return ""


class LanguageController:
    """Text generator window controller"""
    def __init__(self):
        logging.info("Initializing text generator controller")
        self._lm = LanguageModel()
        self._view = GenerateWindow(self)
        self._dialog_back = None

    def run(self):
        self._view.show()

    @staticmethod
    def get_current_model():
        return LanguageModel().name

    def on_click_generate(self):
        try:
            n_words = int(self._view.n_words.text())
            text = str(self._view.text_area.toPlainText())
            gen_text = self._lm.predict(text, n_words)
            self._view.text_area.clear()
            self._view.text_area.insertPlainText(gen_text)
        except ValueError:
            logging.warning("Number of words not specified")
            self._view.text_area.clear()
            self._view.text_area.insertPlainText("Specify the number of words first")
        except TypeError:
            logging.warning("Language model not selected")
            self._view.text_area.clear()
            self._view.text_area.insertPlainText("Choose the language model first")

    def on_click_back(self):
        self._dialog_back = MenuController()
        self._view.close()
        self._dialog_back.run()


class ClassifierController:
    """Review classifier window controller"""
    def __init__(self):
        logging.info("Initializing review classifier controller")
        self._view = ClassifyWindow(self)
        self._clf = Classifier()
        self._dialog_message = MessageController()
        self._dialog_back = None

    def run(self):
        self._view.show()

    @staticmethod
    def get_current_model():
        return Classifier().name

    def on_click_classify(self):
        review = str(self._view.text_area.toPlainText())
        try:
            prediction, proba = self._clf.predict(review)
            self._dialog_message.__setattr__("prediction", prediction)
            self._dialog_message.__setattr__("proba", proba)
            self._dialog_message.run()
        except TypeError:
            logging.warning("Classifier not selected")
            self._view.text_area.clear()
            self._view.text_area.insertPlainText("Choose the classifier first")

    def on_click_back(self):
        self._dialog_back = MenuController()
        self._view.close()
        self._dialog_back.run()


class MessageController:
    """Prediction message alerts controller"""
    def __init__(self):
        logging.info("Initializing message alerts controller")
        self._view = MessageWindow(self)
        self.prediction = ""
        self.proba = 0.0

    def run(self):
        self._view.label.setText(f"Your review was classified as "
                                 f"{self.prediction.upper()} with probability {self.proba * 100:1.2f}%.")

        if self.prediction == "positive":
            self._view.grid_layout.addWidget(self._view.smile, 2, 1)
        else:
            self._view.grid_layout.addWidget(self._view.sad, 2, 1)

        self._view.show()
