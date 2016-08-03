__author__ = 'szeitlin'

import unittest
from Authentication import Authentication

class TestAuthentication(unittest.TestCase):

    def setUp(cls):
        #have to pass in apikey
        cls.base = Authentication(apikey)

    def test_init(self):
        self.assertEqual(self.base.service, "http://umlsks.nlm.nih.gov")

    def test_get_ticketgrantingticket(self):
        self.base.gettgt()
        self.assertTrue(isinstance(self.base.tgt, str))

    def test_get_string(self):
        self.base.getst()
        self.assertTrue(isinstance(self.base.st, str))

class TestRestQuery(unittest.TestCase):

    def test_argument_parsing(self):
        pass


if __name__=='__main__':
    unittest.main()

