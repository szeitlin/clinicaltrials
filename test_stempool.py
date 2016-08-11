__author__ = 'szeitlin'

import pandas as pd
import unittest
from stempool import StemPool

class TestStemPool(unittest.TestCase):

    def setUp(cls):
        argv = "-i lymphoma -s MSH".split()
        cls.pool = StemPool(argv)

    def test_get_df_from_cli(self):
        df = self.pool.get_query_term()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(list(df.columns), ['name', 'ui'])

    def test_fill_stempool(self):
        df = self.pool.get_query_term()
        self.pool.fill_stempool(df)
        self.assertIn('lymphoma', self.pool.stemcounts)

if __name__=='__main__':
    unittest.main()