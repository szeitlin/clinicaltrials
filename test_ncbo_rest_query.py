__author__ = 'szeitlin'

import requests
import unittest
from ncbo_rest_query import (REST_URL,
                             API_KEY,
                             make_request,
                             get_queries,
                            )

class TestNCBOQuery(unittest.TestCase):

    def test_without_authorization(self):
        """
        To see if the link is alive.
        """
        empty_query = requests.get(REST_URL)
        self.assertTrue(isinstance(empty_query.json(), dict))

    def test_with_authorization(self):
        empty_query = make_request("Marrow depression")
        self.assertTrue(isinstance(empty_query, dict))

    def test_search(self):
        query = get_queries(['Marrow depression'])
        self.assertTrue(isinstance(query, list))

if __name__=='__main__':
    unittest.main()

