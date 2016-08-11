#forked from Steve Emrick https://github.com/HHS/uts-rest-api/blob/master/samples/python/retrieve-cui-or-code.py

#################################################################################################
# usage of the script
# usage: python retrieve-cui-or-code.py -k APIKEY -v VERSION -i IDENTIFIER -s SOURCE
# If you do not provide the -s parameter, the script assumes you are retrieving information for a
# known UMLS CUI
#################################################################################################

from Authentication import Authentication
import requests
import json
import argparse
import os
import pandas as pd

class CLI:
    """
    Command-line interface for querying single terms.
    """

    def __init__(self, argv=None):
        """
        :param argv: for testing purposes only

        """
        self.parser = argparse.ArgumentParser(description='process user given parameters')
        #parser.add_argument("-u", "--username", required =  True, dest="username", help = "enter username")
        #parser.add_argument("-p", "--password", required =  True, dest="password", help = "enter passowrd")
        self.parser.add_argument("-k", "--apikey", required = False, dest = "apikey",
                                 default = os.environ.get("APIKEY"),
                                 help = "enter api key from your UTS Profile")
        self.parser.add_argument("-v", "--version", required = False, dest="version",
                                 default = "current", help = "enter version example-2015AA")
        self.parser.add_argument("-i", "--identifier", required = True, dest="identifier",
                                 help = "enter identifier example-C0018787")
        self.parser.add_argument("-s", "--source", required = False, dest="source",
                                 default = 'MSH', help = "enter source name if known")
        self.parser.add_argument("-r", "--returntype", required = False, dest='returntype',
                                 default = "concept",
                                 help = "choose return type (‘aui’,‘concept’,‘code’,\
                                        ‘sourceConcept’,‘sourceDescriptor’, ‘sourceUi’)")

        if argv is not None:
            self.args = self.parser.parse_args(argv)
        else:
            self.args = self.parser.parse_args()

    def cli_authenticate(self):

        #username = args.username
        #password = args.password

        self.AuthClient = Authentication()

    def construct_query(self):

        self.version = self.args.version
        self.identifier = self.args.identifier
        self.source = self.args.source
        self.returntype = self.args.returntype
        self.AuthClient.gettgt()

    def get_query_result(self):
        """
        Search by human-readable string.

        :return: concepts
        """

        self.construct_query()

        uri = "https://uts-ws.nlm.nih.gov"
        content_endpoint = "/rest/search/{0}?string={1}&sabs={2}&returnIdType={3}".format(
                           self.version, self.identifier, self.source, self.returntype)

        self.query = {'ticket':self.AuthClient.getst()}

        r = requests.get(uri+content_endpoint, params=self.query)

        items = json.loads(r.text)
        self.jsonData = items["result"]

        #print(self.jsonData)

        ##uncomment the print statment if you want the raw json output, or you can just look at the documentation :=)
        #https://documentation.uts.nlm.nih.gov/rest/concept/index.html#sample-output
        #https://documentation.uts.nlm.nih.gov/rest/source-asserted-identifiers/index.html#sample-output
        #print (json.dumps(items, indent = 4))

    def parse_query_result(self):
        """
        Extract name and unique id from results.

        :return: pandas dataframe
        """
        results = self.jsonData['results']

        df = pd.DataFrame(results)
        df.drop(['rootSource', 'uri'], axis=1, inplace=True)

        return df

class DirectQuery:
    """
    For piping queries to MSH and building pools of stems from related concepts.

    """
    def __init__(self, identifier):
        """
        :param identifier: (str) search term

        Other attributes are all defaults by design.

        """
        #authorize
        self.AuthClient = Authentication()
        self.AuthClient.gettgt()

        #set attributes
        self.identifier = identifier
        self.version = "current"
        self.source = "MSH"
        self.returntype = "concept"

        #send the query and return dataframe
        self.get_query_result()
        self.df = self.parse_query_result()

    def get_query_result(self):
        """
        Search by human-readable string.

        :return: concepts
        """
        uri = "https://uts-ws.nlm.nih.gov"
        content_endpoint = "/rest/search/{0}?string={1}&sabs={2}&returnIdType={3}".format(
                           self.version, self.identifier, self.source, self.returntype)

        self.query = {'ticket':self.AuthClient.getst()}

        r = requests.get(uri+content_endpoint, params=self.query)

        items = json.loads(r.text)
        self.jsonData = items["result"]

    def parse_query_result(self):
        """
        Extract name and unique id from results.

        :return: pandas dataframe
        """
        results = self.jsonData['results']

        df = pd.DataFrame(results)
        df.drop(['rootSource', 'uri'], axis=1, inplace=True)

        return df


if __name__=='__main__':
    cli = CLI()
    cli.cli_authenticate()
    cli.get_query_result()
    df = cli.parse_query_result()
    print(df.head())
