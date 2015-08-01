import ConfigParser, os, sys

from twisted.application import service, internet
from twisted.internet import reactor
from twisted.python import log

from canarytokend.mysql import MySQLFailedLogins
from canarytokend.canarytoken import Canarytoken
from canarytokend.dnsrequester import DNSRequester

application = service.Application("Canarytokend")

def usage():
    print """
  canarytokend v0.1 -- Thinkst Applied Research (c) 2015

  Usage: twistd -noy canarytokend.tac [ -c configfile ]
  """

def should_create_config():
    while True:
        print "Do you want to create a config file? (Y/n): ",
        r = sys.stdin.readline().strip().lower()
        if r in ['', 'y']:
            return True
        elif r == 'n':
            return False

def get_canarytoken(module=None, email=None):
    ht = Canarytoken()
    return ht.fetch_token(module=module, email=email)

def generate_config(config_path=os.path.expanduser('~/.canarytokend.conf')):
    print """\nWe're going to create a new canarytokend config file."""

    print "First up, where do you want to save the file? "+\
          "({config_path}): ".format(config_path=config_path),
    r = sys.stdin.readline().strip()
    if r == '':
        config_path = config_path
    else:
        config_path = r

    newconfig = ConfigParser.ConfigParser()

    email = None
    print "Do you want to include MySQL failed login tracking? (Y/n): ",
    r = sys.stdin.readline().strip().lower()
    if r in ['', 'y']:
        while True:
            print "Enter the path to the MySQL error log (or enter 'help' "+\
                  "to find it): ",
            error_path = sys.stdin.readline().strip()
            if error_path.lower() == 'help':
                print """
The error log is specified in your MySQL config file (typically found at
/etc/my.cnf, /etc/mysql/my.cnf, or /usr/local/etc/my.cnf.) Inside that config
file, look for the 'log_error' directive. If it is not present, add one:

log_error=mysql.err

The log level should also be a minimum of 2:

log_warnings = 2
#add under the log_error directive

After restarting MySQL, the log will now be present in the data directory,
which can also be found in the MySQL config file stored under the 'datadir'
parameter"""
            else:
                break

        newconfig.add_section('mysql')
        newconfig.set('mysql', 'enabled', True)
        newconfig.set('mysql', 'error_log', error_path)

        ht = Canarytoken()
        ht.fetch_token(module='MySQL', email=email)
        newconfig.set('mysql', 'canary_token', ht.canary_token)
        newconfig.set('mysql', 'dns_token', ht.dns_token)

    print "Writing config file..."
    with open(config_path, 'wb') as config_file:
        newconfig.write(config_file)
    print "Done. Please run canarytokend to read the new config"
    sys.exit(0)


config_files = ['/etc/canarytokend.conf', os.path.expanduser('~/.canarytokend.conf')]

config = ConfigParser.ConfigParser()
files_read = config.read(config_files)

if len(files_read) == 0:
    log.err('No config files found. Searched {files}'.format(files=config_files))
    if should_create_config():
        generate_config()
    else:
        usage()
    sys.exit(-1)

dns_requester = DNSRequester()

if config.has_section('mysql') and config.getboolean('mysql','enabled'):
    MySQLFailedLogins(fileName=config.get('mysql','error_log'),
                      dns_requester=dns_requester,
                      dns_token=config.get('mysql','dns_token')).start()
