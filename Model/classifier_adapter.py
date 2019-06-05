#!/usr/bin/env python3

import numpy as np
from abc import abstractmethod, ABCMeta
from keras.datasets import imdb
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import text_to_word_sequence
from Model.loader import load_fastai_clf, load_keras_clf
import logging


def create_adapter(name):
    """Function to create concrete adapters based on the model name"""
    if "keras" in name:
        return KerasClassifierAdapter(name)
    elif "fastai" in name:
        return FastaiClassifierAdapter(name)
    else:
        logging.warning("Wrong model name")
        raise Exception(f'{name} should contain `keras` or `fastai`')


class ClassifierAdapter(metaclass=ABCMeta):
    """Base adapter for classifier to enable using classifiers trained in different frameworks"""
    def __init__(self):
        logging.debug("Initializing Classifier Adapter")
        self._clf = None
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    @abstractmethod
    def clf(self):
        ...

    @clf.setter
    @abstractmethod
    def clf(self, val):
        ...

    @abstractmethod
    def predict(self, review):
        ...


class KerasClassifierAdapter(ClassifierAdapter):
    """Concrete classifier trained in keras framework"""
    INDEX_FROM = 3
    MAX_WORDS = 500
    DICT_LENGTH = 5000

    def __init__(self, name):
        super().__init__()
        self._clf = load_keras_clf(name)
        self._name = name
        word_index = imdb.get_word_index()
        self.word_to_id = {w: (i + KerasClassifierAdapter.INDEX_FROM) for w, i in word_index.items()}

    @property
    def clf(self):
        return self._clf

    @clf.setter
    def clf(self, name):
        self._clf = load_keras_clf(name)

    def predict(self, review):
        """Return predicted class and probability (>=0.5)"""
        logging.info("Prediction using Keras classifier")
        ppreview = self._prepare_review_to_prediction(review)
        proba = self.clf.predict(ppreview)[0][0]
        return ("positive", proba) if proba > 0.5 else ("negative", 1 - proba)

    def _find_id(self, word):
        return self.word_to_id[word] if word in self.word_to_id.keys() and self.word_to_id[word] < KerasClassifierAdapter.DICT_LENGTH else 0

    def _encode_review(self, review):
        return [self._find_id(word) for word in text_to_word_sequence(review)]

    def _prepare_review_to_prediction(self, review):
        return self._padding((np.array([self._encode_review(review)])))

    @staticmethod
    def _padding(array):
        return pad_sequences(np.array(array), maxlen=KerasClassifierAdapter.MAX_WORDS)


class FastaiClassifierAdapter(ClassifierAdapter):
    """Concrete classifier trained in fastai framework"""
    def __init__(self, name):
        super().__init__()
        self._clf = load_fastai_clf(name)
        self._name = name

    @property
    def clf(self):
        return self._clf

    @clf.setter
    def clf(self, name):
        self._clf = load_fastai_clf(name)

    def predict(self, review):
        """Return predicted class and probability (>=0.5)"""
        logging.info("Prediction using Fastai classifier")
        prediction = self.clf.predict(review)
        proba = prediction[2][1].data.cpu().numpy().round(3)  # cast torch tensor to numpy float value
        return ("positive", proba) if proba > 0.5 else ("negative", 1 - proba)
