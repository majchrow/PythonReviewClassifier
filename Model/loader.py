#!/usr/bin/env python3

from fastai.text import load_learner
from os import listdir
from keras.models import load_model
import logging

# All language models are stored in models/language directory and have `lm` in it
# All classifier are stored in models/classifier directory and have word `clf` in it

PATH_LM = 'models/language/'
PATH_CLF = 'models/classifier/'


def get_all_lm():
    """Return an array of all trained language models"""
    logging.info(f'listing {PATH_LM} directory')
    return [model_name for model_name in listdir(PATH_LM) if 'lm' in model_name]


def get_all_clf():
    """Return an array of all trained classifiers"""
    logging.info(f'listing {PATH_CLF} directory')
    return [model_name for model_name in listdir(PATH_CLF) if 'clf' in model_name]


def load_fastai_lm(lm_name):
    """Return the fastai trained language models"""
    logging.info(f'loading {lm_name} model')
    return load_learner(path=PATH_LM, file=lm_name)


def load_fastai_clf(clf_name):
    """Return the fastai trained classifier"""
    logging.info(f'loading {clf_name} fastai model')
    return load_learner(path=PATH_CLF, file=clf_name)


def load_keras_clf(clf_name):
    """Return the keras trained classifier"""
    logging.info(f'loading {clf_name} keras model')
    return load_model(filepath=PATH_CLF + clf_name)
