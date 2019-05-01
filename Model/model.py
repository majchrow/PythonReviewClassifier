#!/usr/bin/env python3

from functools import wraps
from Model.loader import get_lm, get_clf
from Model.loader import load_lm, load_clf


def singleton(class_):
    instances = {}

    @wraps(class_)
    def wrapper():
        if class_ not in instances:
            instances[class_] = class_()
        return instances[class_]

    return wrapper


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


@singleton
class Classifier:
    """Model to classify movies reviews as good or bad"""

    def __init__(self):
        self._clf = None
        self._clf_name = ""

    @property
    def clf(self):
        return self._clf

    @property
    def clf_name(self):
        return self._clf_name

    @clf.setter
    def clf(self, name):
        if name in get_clf():
            self._clf = load_clf(name)
            self._clf_name = name

    def predict(self, review):
        """Return predicted class and probability (>=0.5)"""
        if self.clf is not None:
            prediction = self.clf.predict(review)
            proba = prediction[2][1].data.cpu().numpy().round(3)  # cast torch tensor to numpy float value
            return ("positive", proba) if proba > 0.5 else ("negative", 1-proba)
