__author__ = 'szeitlin'

import unittest
from Authentication import Authentication
from rest_query import CLI
from argparse import Namespace

class TestAuthentication(unittest.TestCase):

    def setUp(cls):
        #have to pass in apikey from local environment variable
        cls.base = Authentication()

    def test_init(self):
        self.assertEqual(self.base.service, "http://umlsks.nlm.nih.gov")

    def test_get_ticketgrantingticket(self):
        self.base.gettgt()
        self.assertTrue(isinstance(self.base.tgt, str))
        self.assertGreater(len(self.base.tgt), 0)

    def test_get_service_ticket(self):
        self.base.st = self.base.getst()
        self.assertTrue(isinstance(self.base.st, str))


class TestRestQueryCLI(unittest.TestCase):

    def setUp(cls):
        argv = '-i renal -s MSH'.split()
        cls.cli = CLI(argv)

    def test_argument_parsing(self):
        self.assertTrue(isinstance(self.cli.args, Namespace))

    def test_authclient_initialization(self):
        self.cli.cli_authenticate()
        self.assertEqual(self.cli.AuthClient.service, "http://umlsks.nlm.nih.gov")

    def test_construct_query(self):
        self.cli.version = 'current'
        self.cli.identifier = 'renal'
        self.cli.source = 'MEDLINEPLUS'
        self.cli.cli_authenticate()
        self.query = {'ticket':self.cli.AuthClient.getst()}
        self.assertTrue(isinstance(self.query['ticket'], str))

    def test_query_result(self):
        self.cli.cli_authenticate()
        self.cli.construct_query()
        self.cli.jsonData = self.cli.get_query_result()
        self.assertTrue(isinstance(self.cli.jsonData, str))

if __name__=='__main__':
    unittest.main()

