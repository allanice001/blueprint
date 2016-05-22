from ConfigParser import NoOptionError, NoSectionError
import base64
import httplib
import urllib

from blueprint import cfg


try:
    token = cfg.get('librato', 'token')
    username = cfg.get('librato', 'username')
    auth = 'Basic {0}'.format(base64.b64encode('{0}:{1}'.format(username, token)))
except (NoOptionError, NoSectionError):
    auth = None


def count(name, value=1):
    if auth is None:
        return
    conn = httplib.HTTPSConnection('metrics-api.librato.com')
    conn.request('POST',
                 '/v1/counters/{0}.json'.format(urllib.quote(name)),
                 urllib.urlencode({'value': value}),
                 {'Authorization': auth,
                  'Content-Type': 'application/x-www-form-urlencoded'})
    conn.getresponse()
    conn.close()
