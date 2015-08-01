from twisted.names import client
from twisted.python import log

class DNSRequester:

    def print_result(self, result):
        answers, authority, additional = result
        log.msg('DNS lookup returned: {answers}'.format(answers=answers))

    def lookup(self, name=None):
        if not name:
            return
        d = client.lookupAddress(name=name)
        d.addCallback(self.print_result)
