#!/usr/bin/env python3

from Model.loader import get_all_lm
from Model.loader import load_fastai_lm
from abc import abstractmethod, ABCMeta

INDEX_FROM = 3
MAX_WORDS = 500


class LanguageAdapter(metaclass=ABCMeta):
    """Base adapter for language model to enable using models trained in different frameworks"""
    def __init__(self):
        self._lm = None
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    @abstractmethod
    def lm(self):
        ...

    @lm.setter
    @abstractmethod
    def lm(self, val):
        ...

    @abstractmethod
    def predict(self, text, n_words):
        ...


class FastaiAdapter(LanguageAdapter):
    """Concrete language model trained in keras framework"""
    def __init__(self, name):
        super().__init__()
        self._lm = name

    @property
    def lm(self):
        return self._lm

    @lm.setter
    def lm(self, name):
        if name in get_all_lm():
            self._lm = load_fastai_lm(name)

    def predict(self, text, n_words):
        """Return text with n_words that come after text"""
        if self.lm is not None:
            return self.lm.predict(text=text, n_words=n_words, temperature=0.75)
