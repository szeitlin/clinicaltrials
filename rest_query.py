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
        self.parser.add_argument("-v", "--version", required =  False, dest="version",
                                 default = "current", help = "enter version example-2015AA")
        self.parser.add_argument("-i", "--identifier", required =  True, dest="identifier",
                                 help = "enter identifier example-C0018787")
        self.parser.add_argument("-s", "--source", required =  False, dest="source",
                                 help = "enter source name if known")

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

        if self.version is None:
            self.version = 'current'

        uri = "https://uts-ws.nlm.nih.gov"
        content_endpoint = "/rest/content/"+str(self.version)+\
                               "/source/"+str(self.source)+"/"+str(self.identifier)

        self.query = {'ticket':self.AuthClient.getst()}

        r = requests.get(uri+content_endpoint,params=self.query)
        print(r)
        
        r.encoding = 'utf-8'

        items = json.loads(r.text)
        self.jsonData = items["result"]

        ##uncomment the print statment if you want the raw json output, or you can just look at the documentation :=)
        #https://documentation.uts.nlm.nih.gov/rest/concept/index.html#sample-output
        #https://documentation.uts.nlm.nih.gov/rest/source-asserted-identifiers/index.html#sample-output
        #print (json.dumps(items, indent = 4))

    def parse_query_result(self):

        classType = self.jsonData["classType"]
        name = jsonData["name"]
        ui = jsonData["ui"]
        AtomCount = jsonData["atomCount"]
        Definitions = jsonData["definitions"]
        Atoms = jsonData["atoms"]
        DefaultPreferredAtom = jsonData["defaultPreferredAtom"]

        ## print out the shared data elements that are common to both the 'Concept' and 'SourceAtomCluster' class
        print("classType: " + classType)
        print("ui: " + ui)
        print("Name: " + name)
        print("AtomCount: " + str(AtomCount))
        print("Atoms: " + Atoms)
        print("Default Preferred Atom: " + DefaultPreferredAtom)

        ## These data elements may or may not exist depending on what class ('Concept' or 'SourceAtomCluster') you're dealing with so we check for each one.
        try:
           jsonData["definitions"]
           print ("definitions: " + jsonData["definitions"])
        except:
              pass

        try:
           jsonData["parents"]
           print ("parents: " + jsonData["parents"])
        except:
              pass

        try:
           jsonData["children"]
           print ("children: " + jsonData["children"])
        except:
              pass

        try:
           jsonData["relations"]
           print ("relations: " + jsonData["relations"])
        except:
              pass

        try:
           jsonData["descendants"]
           print ("descendants: " + jsonData["descendants"])
        except:
              pass

        try:
           jsonData["semanticTypes"]
           print("Semantic Types:")
           for stys in jsonData["semanticTypes"]:
               print("uri: "+ stys["uri"])
               print("name: "+ stys["name"])

        except:
              pass


if __name__=='__main__':

    cli = CLI(argv)