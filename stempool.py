__author__ = 'szeitlin'


import itertools
from collections import Counter

from nltk.stem.snowball import SnowballStemmer
from rest_query import DirectQuery
from nlp_helpers import apply_word_tokenize

class StemPool:

    def __init__(self, term=None):
        self.dq = DirectQuery(term)
        self.stemmer = SnowballStemmer('english')
        self.df = self.dq.df
        self.stemset = self.fill_stempool()

    def fill_stempool(self):
        """
        Tokenize, flatten, stem, and count.

        :param df: pandas DataFrame of names and unique ids
        :return: self.stemcounts - Counter (dict of {stem (str): count(int)})
        """
        tokens = [apply_word_tokenize(x) for x in self.df['name']]

        flatten1 = itertools.chain.from_iterable
        flat = list(flatten1(tokens))

        stems = [self.stemmer.stem(x) for x in flat]

        return set(stems)


def stemset_combiner(stempool1, stempool2):
    """
    Merge stempools from two sets of terms.

    :param stempool1: (set of str)
    :param stempool2: (set of str)
    :return: bigger stempool
    """
    return stempool1.stemset | stempool2.stemset

#want to group related stems - not sure how to do this yet