#!/usr/bin/env python3

import unittest
import os
from Model.language import LanguageModel
from Model.classifier import Classifier


class TestLanguageModel(unittest.TestCase):
    """Unit tests for Language Model"""
    def test_no_adapter(self):
        lm = LanguageModel()
        with self.assertRaises(TypeError):
            lm.predict("test", 10)

    def test_wrong_name(self):
        os.chdir("..")  # relative to main.py because the paths are relative, do not use this trick more than once
        lm = LanguageModel()
        with self.assertRaises(ValueError):
            lm.lm = "Wrong"

    def test_singleton(self):
        lm = LanguageModel()
        lm2 = LanguageModel()
        self.assertEqual(lm, lm2)


class TestClassifier(unittest.TestCase):
    """Unit tests for Classifier"""
    def test_no_adapter(self):
        clf = Classifier()
        with self.assertRaises(TypeError):
            clf.predict("anything")

    def test_singleton(self):
        clf = Classifier()
        clf2 = Classifier()
        self.assertEqual(clf, clf2)


if __name__ == '__main__':
    unittest.main()
