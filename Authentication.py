
#!/usr/bin/python
#forked from Steve Emrick https://github.com/HHS/uts-rest-api/blob/master/samples/python/Authentication.py
## 5/19/2016 - update to allow for authentication based on api-key, rather than username/pw
## See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
from pyquery import PyQuery as pq
from lxml import etree

uri="https://utslogin.nlm.nih.gov"
#option 1 - username/pw authentication at /cas/v1/tickets
#auth_endpoint = "/cas/v1/tickets/"
#option 2 - api key authentication at /cas/v1/api-key
auth_endpoint = "/cas/v1/api-key"

class Authentication:

    def __init__(self, apikey):
        self.apikey=apikey
        self.service="http://umlsks.nlm.nih.gov"

    def gettgt(self):
        """
        requires an apikey

        :return: tgt (ticket-granting ticket)
        """

        params = {'apikey': self.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        r = requests.post(uri+auth_endpoint,data=params,headers=h)
        d = pq(r.text)
        ## extract the entire URL needed from the HTML form (action attribute) returned

        # looks similar to https://utslogin.nlm.nih.gov/cas/v1/tickets/TGT-36471-aYqNLN2rFIJPXKzxwdTNC5ZT7z3B3cTAKfSc5ndHQcUxeaDOLN-cas
        ## we make a POST call to this URL in the getst method

        self.tgt = d.find('form').attr('action')


    def getst(self):

        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python" }
        r = requests.post(self.tgt,data=params,headers=h)
        self.st = r.text

