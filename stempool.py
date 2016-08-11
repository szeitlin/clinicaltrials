__author__ = 'szeitlin'


import itertools
from collections import Counter

from nltk.stem.snowball import SnowballStemmer
from rest_query import CLI, DirectQuery
from nlp_helpers import apply_word_tokenize

class StemPool:

    def __init__(self, term=None):
        self.dq = DirectQuery(term)
        self.stemmer = SnowballStemmer('english')
        self.df = self.dq.df

    def fill_stempool(self, df):
        """
        Tokenize, flatten, stem, and count.

        :param df: pandas DataFrame of names and unique ids
        :return: self.stemcounts - Counter (dict of {stem (str): count(int)})
        """
        tokens = [apply_word_tokenize(x) for x in df['name']]

        flatten1 = itertools.chain.from_iterable
        flat = list(flatten1(tokens))

        stems = [self.stemmer.stem(x) for x in flat]
        self.stemcounts = Counter(stems)

    def inventory_check(self):
        """
        Check whether terms are already in the stempool.
        If not, add them.

        :return: updated stemcounts
        """
        pass
