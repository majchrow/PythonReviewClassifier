#!/usr/bin/env python3

from Model.singleton import singleton


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
        self._clf = adapter
        self._clf_name = adapter.name

    def predict(self, review):
        if self.clf is not None:
            return self.clf.predict(review)
