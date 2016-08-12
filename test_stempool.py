__author__ = 'szeitlin'

import pandas as pd
import unittest
from stempool import StemPool, stemset_combiner

@unittest.skip("deprecated in favor of DQ protocol")
class TestCLIStemPool(unittest.TestCase):

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

class TestDQStemPool(unittest.TestCase):

    def setUp(cls):
        cls.pool = StemPool("breast")
        cls.pool2 = StemPool("cyst")

    def test_df_exists(self):
        self.assertTrue(isinstance(self.pool.df, pd.DataFrame))
        self.assertEqual(list(self.pool.df.columns), ['name', 'ui'])

    def test_fill_stempool(self):
        self.assertIn('breast', self.pool.stemset)

    @unittest.skip("deprecated")
    def test_inventory_check(self):
        self.pool.fill_stempool(self.pool.df)
        self.pool.inventory_check('lymphoma')
        self.assertNotIn('lymphoma', self.pool.stemcounts)
        pre = self.pool.stemcounts.get('cyst')
        self.pool.inventory_check('cyst')
        post = self.pool.stemcounts.get('cyst')
        self.assertGreater(post, pre)

    def test_stemset_combiner(self):
        self.assertTrue(isinstance(self.pool2.stemset, set))
        bigger = stemset_combiner(self.pool, self.pool2)
        self.assertTrue(isinstance(bigger, set))
        self.assertGreater(len(bigger), len(self.pool.stemset))

if __name__=='__main__':
    unittest.main()