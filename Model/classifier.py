#!/usr/bin/env python3

from Model.singleton import singleton


@singleton
class Classifier:
    """Common model to classify movies reviews as good or bad"""

    def __init__(self):
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
            return self.clf.predict(review)
        else:
            raise Exception('`classifier` was not selected')
