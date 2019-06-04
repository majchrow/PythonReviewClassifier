import numpy as np
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

seed = 7
np.random.seed(seed)
INDEX_FROM = 3
TOP_WORDS = 5000
MAX_WORDS = 500


def train_and_save_simple(path):
    """Train and save multi-layer perceptron model"""
    (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=TOP_WORDS, index_from=INDEX_FROM)
    X_train = sequence.pad_sequences(X_train, maxlen=MAX_WORDS)
    X_test = sequence.pad_sequences(X_test, maxlen=MAX_WORDS)
    model = Sequential()
    model.add(Embedding(TOP_WORDS, 32, input_length=MAX_WORDS))
    model.add(Flatten())
    model.add(Dense(250, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=2, batch_size=128, verbose=2)
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))
    model.save(path)


def train_and_save_cnn(path):
    """Train and save multi-layer perceptron model"""
    (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=TOP_WORDS, index_from=INDEX_FROM)
    X_train = sequence.pad_sequences(X_train, maxlen=MAX_WORDS)
    X_test = sequence.pad_sequences(X_test, maxlen=MAX_WORDS)
    model = Sequential()
    model.add(Embedding(TOP_WORDS, 32, input_length=TOP_WORDS))
    model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(250, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=2, batch_size=128, verbose=2)
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))
    model.save(path)

