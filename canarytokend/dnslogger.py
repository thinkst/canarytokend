import base64
import random

from twisted.python import log as tlog

class DNSLogger:
    MAX_LABEL_SIZE=63

    def log(self, msg=None):
        tlog.msg('Logging: {msg}'.format(msg=msg))

        if not hasattr(self, 'dns_requester'):
            raise Exception('Log module has no dns_requester assigned. Did you'+\
                            'forget it in the module\'s __init__() perhaps?')

        #ensure the message fits into a query. if not, shave off the front 
        #of the message until it does.
        while True:
            hostname = self.dns_token
            if msg:
                #replace non-DNS char (=), and break up into 64-char chunks
                reverse_msg = base64.b32encode(msg).replace('=','-')[::-1]
                hostname = '.M{:03}.'.format(random.randint(0,999)) + hostname
                hostname = '.'.join([ reverse_msg[i:i+self.MAX_LABEL_SIZE] 
                                      for i in range(0, len(reverse_msg),
                                                     self.MAX_LABEL_SIZE) 
                                               ])[::-1] + hostname

            if len(hostname) <= 253:
                break

            msg = msg[1:]

        tlog.msg('Requesting : {hostname}'.format(hostname=hostname))
        self.dns_requester.lookup(name=hostname)
