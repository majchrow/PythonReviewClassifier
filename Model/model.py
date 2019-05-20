#!/usr/bin/env python3

from functools import wraps
from keras.datasets import imdb
from Model.loader import get_lm, get_clf
from Model.loader import load_lm, load_clf, load_keras
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence
import numpy as np


INDEX_FROM = 3
MAX_WORDS = 500

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
    def clf(self, adapter):
        #if name in get_clf():
            self._clf = adapter
            self._clf_name = adapter.name
            #self._clf_name = name

    def predict(self, review):
        if self.clf is not None:
            return self.clf.predict(review)


class Adapter:
    def predict(self, review):
        pass


@singleton
class KerasAdapter(Adapter):
    def __init__(self, name):
        self.clf = load_keras(name)
        self._name = name
        word_index = imdb.get_word_index()
        self.word_to_id = {w: (i+INDEX_FROM) for w, i in word_index.items()}

    @property
    def name(self):
        return self.name

    def predict(self, review):
        ppreview = self.prepare_review_to_prediction(review)
        proba = self.clf.predict(ppreview)[0][0]
        return ("positive", proba) if proba > 0.5 else ("negative", 1 - proba)

    def find_id(self, word):
        if word in self.word_to_id.keys():
            return self.word_to_id[word]
        else:
            return 0

    def encode_review(self, review):
        return [self.find_id(word) for word in text_to_word_sequence(review)]

    def prepare_review_to_prediction(self, review):
        return self.padding((np.array([self.encode_review(review)])))

    @staticmethod
    def padding(array):
        return sequence.pad_sequences(np.array(array), maxlen=MAX_WORDS)


@singleton
class FastaiAdapter(Adapter):
    def __init__(self, name):
        self.clf = load_clf(name)
        self.name = name

    def name(self):
        return self.name

    def predict(self, review):
        """Return predicted class and probability (>=0.5)"""
        prediction = self.clf.predict(review)
        proba = prediction[2][1].data.cpu().numpy().round(3)  # cast torch tensor to numpy float value
        return ("positive", proba) if proba > 0.5 else ("negative", 1 - proba)

