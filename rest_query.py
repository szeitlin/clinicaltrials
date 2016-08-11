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

class CLI:

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
                                 help = "enter source name if known")
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

        # try:
        #    source
        # except NameError:
        #    source = None
        #
        # ##if we don't specify a source vocabulary, assume we're retrieving UMLS CUIs
        # if source is None:
        #     content_endpoint = "/rest/content/"+str(self.version)+"/CUI/"+str(self.identifier)

    def get_query_result(self):
        """
        Search by human-readable string.

        :return: concepts
        """

        self.construct_query()

        uri = "https://uts-ws.nlm.nih.gov"
        content_endpoint = "/rest/search/{0}?string={1}&sabs={2}&returnIdType={3}".format(
                           self.version, self.identifier, self.source, self.returntype)

        #endpoint = "/rest/search/current?string={0}".format(self.identifier)

        self.query = {'ticket':self.AuthClient.getst()}

        print(uri+content_endpoint)

        r = requests.get(uri+content_endpoint, params=self.query)
        #r = requests.get(uri + endpoint, params=self.query)
        print(r.status_code)
        #print(r.text)

        items = json.loads(r.text)
        self.jsonData = items["result"]

        print(self.jsonData)

        ##uncomment the print statment if you want the raw json output, or you can just look at the documentation :=)
        #https://documentation.uts.nlm.nih.gov/rest/concept/index.html#sample-output
        #https://documentation.uts.nlm.nih.gov/rest/source-asserted-identifiers/index.html#sample-output
        #print (json.dumps(items, indent = 4))

    # def parse_query_result(self):
    #
    #     jsonData = self.jsonData
    #
    #     classType = jsonData["classType"]
    #     name = jsonData["name"]
    #     ui = jsonData["ui"]
    #     AtomCount = jsonData["atomCount"]
    #     Definitions = jsonData["definitions"]
    #     Atoms = jsonData["atoms"]
    #     DefaultPreferredAtom = jsonData["defaultPreferredAtom"]
    #
    #     ## print out the shared data elements that are common to both the 'Concept' and 'SourceAtomCluster' class
    #     print("classType: " + classType)
    #     print("ui: " + ui)
    #     print("Name: " + name)
    #     print("AtomCount: " + str(AtomCount))
    #     print("Atoms: " + Atoms)
    #     print("Default Preferred Atom: " + DefaultPreferredAtom)
    #
    #     ## These data elements may or may not exist depending on what class ('Concept' or 'SourceAtomCluster') you're dealing with so we check for each one.
    #     try:
    #        print ("definitions: " + jsonData["definitions"])
    #     except:
    #           pass
    #
    #     try:
    #        print ("parents: " + jsonData["parents"])
    #     except:
    #           pass
    #
    #     try:
    #        print ("children: " + jsonData["children"])
    #     except:
    #           pass
    #
    #     try:
    #        print ("relations: " + jsonData["relations"])
    #     except:
    #           pass
    #
    #     try:
    #        print ("descendants: " + jsonData["descendants"])
    #     except:
    #           pass
    #
    #     try:
    #        print("Semantic Types:")
    #        for stys in jsonData["semanticTypes"]:
    #            print("uri: "+ stys["uri"])
    #            print("name: "+ stys["name"])
    #
    #     except:
    #           pass


if __name__=='__main__':
    cli = CLI()