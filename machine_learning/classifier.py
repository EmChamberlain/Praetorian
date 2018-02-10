import binascii
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from sklearn.decomposition import PCA

import numpy as np
import matplotlib.pyplot as plt


class Classifier:
    data_train = None
    target_train = None
    def __init__(self, data_in, targets_in):
        self.target_train = targets_in
        self.data_train = data_in
        # print(len(self.data_train))


    def train(self):
        # taken directly from the tutorial
        # I didn't know you could do this with python arguments, it is actually very cool
        vec_opts = {
            "ngram_range": (1, 4),  # allow n-grams of 1-4 words in length (32-bits)
            "analyzer": "word",  # analyze hex words
            "token_pattern": "..",  # treat two characters as a word (e.g. 4b)
            "min_df": 0.1,  # for demo purposes, be very selective about features
        }
        idf_opts = {"use_idf": True}

        v = CountVectorizer(**vec_opts)
        idf = TfidfTransformer(**idf_opts)

        # X is going to be a sparse matrix of the number of occurrences of different features from the CountVectorizer
        X = v.fit_transform(self.data_train, self.target_train)
        print(X.shape[1])
        X = idf.fit_transform(X)
        print(X.shape[1])

        pca = PCA()
        X = pca.fit_transform(X.toarray())
        print(X)

        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']

        for color, i, target_name in zip(colors, range(X.shape[1]), self.target_train):
            plt.scatter(X[:, 0], X[:, 1], color=color, alpha=.8, lw=2,
                        label=target_name)
        plt.legend(loc='best', shadow=False, scatterpoints=1)
        plt.title('PCA of IRIS dataset')
        plt.show()
