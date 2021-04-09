import os
import sys

sys.path.insert(0, "/home/emptytxt/public_html/pizookies/pythonprojects/continuum")
os.chdir("/home/emptytxt/public_html/pizookies/pythonprojects/continuum")
os.environ['DJANGO_SETTINGS_MODULE'] = "continuum.settings"

from continuum.wsgi import application
from flup.server.fcgi import WSGIServer
if __name__ == '__main__':
    WSGIServer(application).run()