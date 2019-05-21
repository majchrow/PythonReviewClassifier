import sys
import Model.loader
from Model.model import Classifier, LanguageModel
from View.view import StartWindow, MenuWindow, ChooseWindow, GenerateWindow, ClassifyWindow, MessageWindow
from PyQt5.QtWidgets import QApplication
from Model.adapters import create_adapter


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

    def on_click_apply_clf(self):
        clf = self._view.combo_box_clf.currentText()
        self._clf.clf = create_adapter(clf)
        self._view.current_clf.setText(clf)

    def on_click_apply_lm(self):
        lm = self._view.combo_box_lm.currentText()
        self._lm.lm = lm
        self._view.current_lm.setText(self._lm.lm_name)

    def on_click_back(self):
        self.dialog_back = MenuController()
        self._view.close()
        self.dialog_back.run()

    def get_current_lm(self):
        if self._lm is not None:
            return self._lm.lm_name
        else:
            return ""

    def get_current_clf(self):
        if self._clf is not None:
            return self._clf.clf_name
        else:
            return ""


class LanguageController:
    def __init__(self):
        self._lm = LanguageModel()
        self._view = GenerateWindow(self)
        self._dialog_back = None

    def run(self):
        self._view.show()

    @staticmethod
    def get_current_model():
        return LanguageModel().lm_name

    def on_click_generate(self):
        n_words = int(self._view.n_words.text())
        text = str(self._view.text_area.toPlainText())
        gen_text = self._lm.predict(text, n_words)
        self._view.text_area.clear()
        self._view.text_area.insertPlainText(gen_text)

    def on_click_back(self):
        self._dialog_back = MenuController()
        self._view.close()
        self._dialog_back.run()


class ClassifierController:
    def __init__(self):
        self._view = ClassifyWindow(self)
        self._clf = Classifier()
        self._dialog_message = MessageController()
        self._dialog_back = None

    def run(self):
        self._view.show()

    @staticmethod
    def get_current_model():
        return Classifier().clf_name

    def on_click_classify(self):
        review = str(self._view.text_area.toPlainText())
        prediction, proba = self._clf.predict(review)
        self._dialog_message.__setattr__("prediction", prediction)
        self._dialog_message.__setattr__("proba", proba)
        self._dialog_message.run()

    def on_click_back(self):
        self._dialog_back = MenuController()
        self._view.close()
        self._dialog_back.run()


class MessageController:
    def __init__(self):
        self._view = MessageWindow(self)
        self.prediction = ""
        self.proba = 0.0

    def run(self):
        self._view.label.setText(f"Your review was classified as "
                                 f"{self.prediction.upper()} with probability {self.proba * 100:1.2f}%.")

        if self.prediction == "positive":
            self._view.grid_layout.addWidget(self._view.smile, 2, 2)
        else:
            self._view.grid_layout.addWidget(self._view.sad, 2, 2)

        self._view.show()
