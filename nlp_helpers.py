__author__ = 'szeitlin'

import nltk

def apply_word_tokenize(x):
    """ Tokenize
        :param: x (str)
        :return: token (list of str)
    """
    words = nltk.word_tokenize(x.lower())
    return words

