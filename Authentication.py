
#!/usr/bin/python
#forked from Steve Emrick https://github.com/HHS/uts-rest-api/blob/master/samples/python/Authentication.py
## 5/19/2016 - update to allow for authentication based on api-key, rather than username/pw
## See https://documentation.uts.nlm.nih.gov/rest/authentication.html for full explanation

import requests
from pyquery import PyQuery as pq
import os

uri="https://utslogin.nlm.nih.gov"
#option 1 - username/pw authentication at /cas/v1/tickets
#auth_endpoint = "/cas/v1/tickets/"
#option 2 - api key authentication at /cas/v1/api-key
auth_endpoint = "/cas/v1/api-key"

#to save apikey locally, do `export APIKEY="apikeytexthere"`

class Authentication:

    def __init__(self):
        self.apikey=os.environ.get("APIKEY")
        self.service="http://umlsks.nlm.nih.gov"
        self.gettgt()

    def gettgt(self):
        """
        requires an apikey

        TGT can be re-used.

        :return: tgt (ticket-granting ticket)
        """

        params = {'apikey': self.apikey}
        h = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain", "User-Agent":"python" }
        r = requests.post(uri+auth_endpoint,data=params,headers=h)
        d = pq(r.text)
        ## extract the entire URL needed from the HTML form (action attribute) returned

        # looks similar to https://utslogin.nlm.nih.gov/cas/v1/tickets/TGT-36471-aYqNLN2rFIJPXKzxwdTNC5ZT7z3B3cTAKfSc5ndHQcUxeaDOLN-cas
        ## we make a POST call to this URL in the getst method

        tgt = d.find('form').attr('action')
        self.tgt = tgt

        #print(type(self.tgt))
        #print(isinstance(self.tgt, str))

    def getst(self):
        """
        requires a ticket-granting ticket

        Service Ticket CANNOT be re-used.

        :return: st (service ticket)

        """
        params = {'service': self.service}
        h = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "User-Agent":"python"}
        r = requests.post(self.tgt, data=params, headers=h)

        print(r.text)

        return r.text

