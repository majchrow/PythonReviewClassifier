#!/usr/bin/env python3

from fastai.text import load_learner
from os import listdir
from keras.models import load_model

# All language models are stored in models/language directory
# All classifier are stored in models/classifier directory

PATH_LM = 'models/language/'
PATH_CLF = 'models/classifier/'


def get_lm():
    """Return an array of all trained language models"""
    return [model_name for model_name in listdir(PATH_LM) if 'lm' in model_name]


def get_clf():
    """Return an array of all trained classifiers"""
    return [model_name for model_name in listdir(PATH_CLF) if 'clf' in model_name]


def load_lm(lm_name):
    """Return the trained language models"""
    return load_learner(path=PATH_LM, file=lm_name)


def load_clf(clf_name):
    """Return the trained classifier"""
    return load_learner(path=PATH_CLF, file=clf_name)


def load_keras(clf_name):
    """Return the trained classifier"""
    return load_model(filepath=PATH_CLF+clf_name)