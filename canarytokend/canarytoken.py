import sys
import requests

class Canarytoken(object):
    
    def _setup_token(self,module=None, email=None):
        print "Generating a new canarytoken for {module}".format(module=module)
        while True:
            if not email:
                print "Please enter an email address for receiving alerts: ",
                self.email = sys.stdin.readline().strip()
            else:
                print "Please enter an email address for receiving alerts "+\
                      "({email}): ".format(email=email),
                self.email = sys.stdin.readline().strip()
                if len(self.email) == 0:
                    self.email = email
            if len(self.email) > 0:
                break

        print "Please enter a short description to remind you about this token: ",
        self.memo = sys.stdin.readline().strip()

    def _request_token(self,):
        resp = requests.post('http://canarytokens.org/generate', 
                             params={'email':self.email,'memo':self.memo})
        resp = resp.json()
        if resp['Error'] is not None:
            raise Exception('An error occurred requesting token: {errorcode}'\
                            .format(errorcode=resp['Error']))
        if resp['Token'] == '':
            raise Exception('An error occurred request token: {error}'\
                            .format(error='No token was returned'))
        self.dns_token = resp['Hostname']
        self.canary_token = resp['Token']

    def fetch_token(self, module=None, email=None):
        self._setup_token(module=module, email=email)
        self._request_token()
        return self
