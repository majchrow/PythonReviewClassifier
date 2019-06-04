#!/usr/bin/env python3

from Model.singleton import singleton
import logging


@singleton
class Classifier:
    """Common model to classify movies reviews as good or bad"""

    def __init__(self):
        logging.debug("Initializing common classifier")
        self._clf = None
        self._name = None

    @property
    def clf(self):
        return self._clf

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @clf.setter
    def clf(self, adapter):
        self._clf = adapter
        self.name = adapter.name

    def predict(self, review):
        """Return predicted class and probability (>=0.5) by calling predict on concrete adapter"""
        if self.clf is not None:
            logging.info(f"Model {self.name} is predicting review: {review}")
            return self.clf.predict(review)
        else:
            logging.warning('Trying to predict review without selected classifier')
            raise TypeError('`classifier` was not selected')
