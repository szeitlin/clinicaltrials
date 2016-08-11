__author__ = 'szeitlin'

import unittest
from Authentication import Authentication
from rest_query import CLI, DirectQuery
from argparse import Namespace
import requests
import pandas as pd

class TestAuthentication(unittest.TestCase):

    def setUp(cls):
        #have to pass in apikey from local environment variable
        cls.base = Authentication()

    def test_init(self):
        self.assertEqual(self.base.service, "http://umlsks.nlm.nih.gov")

    def test_get_ticketgrantingticket(self):
        self.assertTrue(isinstance(self.base.tgt, str))
        self.assertGreater(len(self.base.tgt), 0)

    def test_get_service_ticket(self):
        self.base.st = self.base.getst()
        self.assertTrue(isinstance(self.base.st, str))

    def test_validate_service_ticket(self):
        self.base.st = self.base.getst()
        uri = "https://utslogin.nlm.nih.gov" #this has to be https!
        endpoint = "/cas/serviceValidate?ticket={}&service={}".format(self.base.st, self.base.service)
        params = {'apikey': self.base.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain", "User-Agent":"python"}
        r = requests.get(uri+endpoint, data=params, headers=h)
        self.assertEqual(r.status_code, 200)

class TestRestQueryCLI(unittest.TestCase):

    def setUp(cls):
        argv = '-i idiopathic -s MSH'.split()
        cls.cli = CLI(argv)

    def test_argument_parsing(self):
        self.assertTrue(isinstance(self.cli.args, Namespace))

    def test_authclient_initialization(self):
        self.cli.cli_authenticate()
        self.assertEqual(self.cli.AuthClient.service, "http://umlsks.nlm.nih.gov")

    def test_construct_query(self):
        self.cli.version = 'current'
        self.cli.identifier = 'cardiac'
        self.cli.source = 'All Sources'
        self.cli.cli_authenticate()
        self.query = {'ticket':self.cli.AuthClient.getst()}
        self.assertTrue(isinstance(self.query['ticket'], str))

    def test_query_result(self):
        self.cli.cli_authenticate()
        self.assertEqual(self.cli.AuthClient.service, "http://umlsks.nlm.nih.gov")
        self.cli.get_query_result()
        self.assertTrue(isinstance(self.cli.query['ticket'], str))
        self.assertTrue(isinstance(self.cli.jsonData, dict))

    def parse_query_result(self):
        self.cli.cli_authenticate()
        self.cli.get_query_result()
        df = self.cli.parse_query_result()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.columns, ['name', 'ui'])

class TestDirectQuery(unittest.TestCase):

    def test_direct_query(self):
        dq = DirectQuery("breast")
        self.assertTrue(isinstance(dq.df, pd.DataFrame))
        self.assertEqual(list(dq.df.columns), ['name', 'ui'])

if __name__=='__main__':
    unittest.main()

