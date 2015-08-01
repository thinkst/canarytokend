import re

from twisted.python import log as tlog

from canarytokend.filesystemwatcher import FileSystemWatcher
from canarytokend.dnslogger import DNSLogger


class MySQLFailedLogins(FileSystemWatcher, DNSLogger):
    def __init__(self, dns_requester=None, fileName=None, dns_token=None):
        super(MySQLFailedLogins, self).__init__(fileName=fileName)
        self.dns_token = dns_token#.split('.', 1)[1]
        self.dns_requester = dns_requester
        self.line_re = re.compile(".*Access denied for user '([^']*)'@'([^']*)'.*")

    def handleLines(self, lines=None):
        tlog.msg('Got lines: {lines}'.format(lines=lines))

        for line in lines:
            m = self.line_re.match(line)
            if m:
                self.log(m.group(1))
