__author__ = 'szeitlin'

#forked from template code at https://github.com/ncbo/ncbo_rest_sample_code/blob/master/python/classes_search.py


#import urllib2 #switch to using requests
import requests
import json
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = os.environ.get("NCBO_APIKEY")

#to save apikey locally, do `export NCBO_APIKEY="apikeytexthere"`

def make_request(term):
    """

    Helper method with newer HTTP library.

    :param url:
    :return: json object
    """
    h = {'Authorization' : 'apikey token=' + API_KEY}
    r = requests.post(REST_URL + "/search?q=" + term, headers=h)

    if r.status_code is not 200:
        print(r.status_code)
    else:
        return r.json()

def get_search_terms_from_file(filename):
    """
    Not sure I would actually use this at all.

    :param filename:
    :return:
    """
    path = os.path.join(os.path.dirname(__file__), filename)
    terms_file = open(path, "r")
    terms = []
    for line in terms_file:
        terms.append(line)

def get_queries(terms):
    """
    Actually runs the queries

    :param terms: list of search terms
    :return: list of json objects
    """
    search_results = []
    for term in terms:
        search_results.append(make_request(term)["collection"])

    return search_results

def print_results(search_results):
    """
    Helper method

    :param search_results:
    :return: none
    """
    for result in search_results:
        pprint(result)