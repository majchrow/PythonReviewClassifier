#!/usr/bin/env python3

from Model.loader import get_all_lm
from Model.loader import load_fastai_lm
from Model.singleton import singleton


@singleton
class LanguageModel:
    """Language Model to predicts next words in a sentence. Used to generate text."""

    def __init__(self):
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
            return self.lm.predict(text=text, n_words=n_words)
