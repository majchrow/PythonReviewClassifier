#!/usr/bin/env python3

import logging
from fastai.text import URLs, TextList, untar_data
from fastai.text import language_model_learner, text_classifier_learner, AWD_LSTM

bs = 32
ENCODER_PATH = '../Tmp/encoder'
LM_PATH = '../models/language/fastai_base_lm.pkl'
CLF_PATH = '../models/classifier/fastai_base_clf.pkl'


def train_fastai_language(save_encoder=True):
    """Train base fastai language pretrained model and save to the proper folder

    :param save_encoder: if true, save encoder(needed for classifier) as well
    """
    logging.info("Starting fastai language model training")
    path = untar_data(URLs.IMDB)
    logging.info("Loading data")
    data_lm = (TextList.from_folder(path)
               .filter_by_folder(include=['train', 'test', 'unsup'])
               .random_split_by_pct(0.1)
               .label_for_lm()
               .databunch(bs=bs))
    lm_lerner = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)
    logging.info("Starting training")
    lm_lerner.freeze()
    lm_lerner.fit_one_cycle(1, 5e-2, moms=(0.8, 0.7))
    lm_lerner.unfreeze()
    lm_lerner.fit_one_cycle(2, 1e-6, moms=(0.8, 0.7))
    logging.info("Training done, saving model")
    lm_lerner.save(LM_PATH)
    if save_encoder:
        logging.info("Saving encoder")
        lm_lerner.save_encoder(ENCODER_PATH)


def save_encoder_from_trained():
    """Save encoder to Tmp folder if language model is already trained"""
    logging.info("Saving encoder from trained language model")
    path = untar_data(URLs.IMDB)
    data_lm = (TextList.from_folder(path)
               .filter_by_folder(include=['train', 'test', 'unsup'])
               .random_split_by_pct(0.1)
               .label_for_lm()
               .databunch(bs=bs))
    lm_lerner = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)
    try:
        lm_lerner.load(LM_PATH)
    except FileNotFoundError:
        logging.warning("Language model is not trained")
        raise FileNotFoundError("Language model not trained")
    lm_lerner.save_encoder(ENCODER_PATH)


def train_fastai_classifier():
    """Train base fastai classifier using pretrained model and trained language model encoder
       and save it to the proper folder"""
    logging.info("Starting fastai classifier training")
    path = untar_data(URLs.IMDB)
    logging.info("Loading data")
    data_lm = (TextList.from_folder(path)
               .filter_by_folder(include=['train', 'test', 'unsup'])
               .random_split_by_pct(0.1)
               .label_for_lm()
               .databunch(bs=bs))
    data_class = (TextList.from_folder(path, vocab=data_lm.vocab)
                  .split_by_folder(valid='test')
                  .label_from_folder(classes=['neg', 'pos'])
                  .databunch(bs=bs))
    logging.info("Loading model")
    clf_learner = text_classifier_learner(data_class, AWD_LSTM, drop_mult=0.5)
    try:
        clf_learner.load_encoder(ENCODER_PATH)
    except FileNotFoundError:
        logging.warning("No encoder trained")
        try:
            save_encoder_from_trained()
            clf_learner.load_encoder(ENCODER_PATH)
        except FileNotFoundError:
            logging.warning("No language model trained")
            logging.info("Training language model to get the encode")
            train_fastai_language(save_encoder=True)
            clf_learner.load_encoder(ENCODER_PATH)
    logging.info("Starting training")
    clf_learner.freeze()
    clf_learner.fit_one_cycle(1, 2e-2, moms=(0.8, 0.7))
    clf_learner.freeze_to(-2)
    clf_learner.fit_one_cycle(1, slice(1e-2 / (2.6 ** 4), 1e-2), moms=(0.8, 0.7))
    clf_learner.freeze_to(-3)
    clf_learner.fit_one_cycle(1, slice(5e-3 / (2.6 ** 4), 5e-3), moms=(0.8, 0.7))
    clf_learner.unfreeze()
    clf_learner.fit_one_cycle(5, slice(1e-3 / (2.6 ** 4), 1e-3), moms=(0.8, 0.7))
    logging.info("Training done, saving model")
    clf_learner.export(CLF_PATH)


if __name__ == "__main__":
    logging.basicConfig(filename='../Tmp/logfile.log', level=logging.DEBUG)
    train_fastai_language(save_encoder=True)
    train_fastai_classifier()
