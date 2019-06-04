#!/usr/bin/env python3

from Model.loader import get_all_lm
from Model.loader import load_fastai_lm
from Model.singleton import singleton
import logging


@singleton
class LanguageModel:
    """Language Model to predicts next words in a sentence. Used to generate text."""
    def __init__(self):
        logging.info("Initializing common language model")
        self._lm = None
        self._name = None

    @property
    def lm(self):
        return self._lm

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @lm.setter
    def lm(self, name):
        if name in get_all_lm():
            self._lm = load_fastai_lm(name)
            self.name = name

    def predict(self, text, n_words):
        """Return text with n_words that come after text"""
        if self.lm is not None:
            logging.info(f"Model {self.name} is predicting {n_words} after {text}")
            return self.lm.predict(text=text, n_words=n_words)
        else:
            logging.warning('Trying to generate text without selected language model')
            raise TypeError('`language model` was not selected')
