#!/usr/bin/env python3

from Model.loader import get_lm
from Model.loader import load_lm
from Model.singleton import singleton


@singleton
class LanguageModel:
    """Language Model to predicts next words in a sentence. Used to generate text."""

    def __init__(self):
        self._lm = None
        self._lm_name = ""

    @property
    def lm(self):
        return self._lm

    @property
    def lm_name(self):
        return self._lm_name

    @lm.setter
    def lm(self, name):
        if name in get_lm():
            self._lm = load_lm(name)
            self._lm_name = name

    def predict(self, text, n_words=50, temperature=0.75):
        """Return text with n_words that come after text"""
        if self.lm is not None:
            return self.lm.predict(text=text, n_words=n_words, temperature=temperature)
