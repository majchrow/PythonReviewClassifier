import numpy as np
from abc import abstractmethod, ABCMeta
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.preprocessing.text import text_to_word_sequence
from Model.loader import load_clf, load_keras

INDEX_FROM = 3
MAX_WORDS = 500


class Adapter(metaclass=ABCMeta):
    def __init__(self):
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


class KerasAdapter(Adapter):
    def __init__(self, name):
        super().__init__()
        self._clf = load_keras(name)
        self._name = name
        word_index = imdb.get_word_index()
        self.word_to_id = {w: (i + INDEX_FROM) for w, i in word_index.items()}

    @property
    def clf(self):
        return self._clf

    @clf.setter
    def clf(self, name):
        self._clf = load_keras(name)

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


class FastaiAdapter(Adapter):
    def __init__(self, name):
        super().__init__()
        self._clf = load_clf(name)
        self._name = name

    @property
    def clf(self):
        return self._clf

    @clf.setter
    def clf(self, name):
        self._clf = load_clf(name)

    def predict(self, review):
        """Return predicted class and probability (>=0.5)"""
        prediction = self.clf.predict(review)
        proba = prediction[2][1].data.cpu().numpy().round(3)  # cast torch tensor to numpy float value
        return ("positive", proba) if proba > 0.5 else ("negative", 1 - proba)


def create_adapter(name):
    if "keras" in name:
        return KerasAdapter(name)
    else:
        return FastaiAdapter(name)
