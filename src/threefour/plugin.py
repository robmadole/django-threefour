import os
from time import sleep

import nose
from selenium.remote import connect
from selenium.common.exceptions import NoSuchElementException
from nose.plugins import Plugin
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import AdminMediaHandler
from django.test import utils
from django.db import connection

DEFAULT_LIVE_SERVER_PROTOCOL = "http"
DEFAULT_LIVE_SERVER_PORT = 8000
DEFAULT_LIVE_SERVER_ADDRESS = '0.0.0.0'
DEFAULT_URL_ROOT_SERVER_ADDRESS = 'localhost'


def get_test_case_class(nose_test):
    if isinstance(nose_test.test, nose.case.MethodTestCase):
        return nose_test.test.test.im_class
    else:
        return nose_test.test.__class__


def get_test_case_instance(nose_test):
    if isinstance(nose_test.test, nose.case.MethodTestCase):
        return nose_test.test.test.im_self
    else:
        return None


def enable_test(test_case, plugin_attribute):
    if not getattr(test_case, plugin_attribute, False):
        setattr(test_case, plugin_attribute, True)


class ServerPlugin(Plugin):
    name = 'threefour'
    activation_parameter = '--with-threefour'

    def __init__(self):
        Plugin.__init__(self)
        self.server_started = False
        self.server_thread = None

    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)

    def configure(self, options, config):
        Plugin.configure(self, options, config)

    def begin(self):
        utils.setup_test_environment()
        self._old_db_name = connection.creation.create_test_db(verbosity=1)

    def finalize(self, *args, **kwargs):
        connection.creation.destroy_test_db(self._old_db_name)
        utils.teardown_test_environment()
    
    def start_server(self, address='0.0.0.0', port=8000):
         _application = AdminMediaHandler(WSGIHandler())
    
         def application(environ, start_response):
             environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
             return _application(environ, start_response)
    
         from cherrypy.wsgiserver import CherryPyWSGIServer
         from threading import Thread
         self.httpd = CherryPyWSGIServer((address, port), application, server_name='django-test-http')
         self.httpd_thread = Thread(target=self.httpd.start)
         self.httpd_thread.start()
         #FIXME: This could be avoided by passing self to thread class starting django
         # and waiting for Event lock
         sleep(.5)

    def stop_server(self):
        if self.server_started:
            self.httpd.stop()
            self.server_started = False

    def check_database_multithread_compilant(self):
        # When using memory database, complain as we'd use indepenent databases
        from django.conf import settings
        if settings.DATABASE_ENGINE == 'sqlite3' \
            and (not getattr(settings, 'TEST_DATABASE_NAME', False) or settings.TEST_DATABASE_NAME == ':memory:'):
            self.skipped = True
            return False
            #raise SkipTest("You're running database in memory, but trying to use live server in another thread. Skipping.")
        return True

    def startTest(self, test):
        from django.conf import settings
        test_case = get_test_case_class(test)
        test_instance = get_test_case_instance(test)
        if not self.server_started and getattr(test_case, "start_live_server", False):
            if not self.check_database_multithread_compilant():
                return
            self.start_server(
                address=getattr(settings, "LIVE_SERVER_ADDRESS", DEFAULT_LIVE_SERVER_ADDRESS),
                port=int(getattr(settings, "LIVE_SERVER_PORT", DEFAULT_LIVE_SERVER_PORT))
            )
            self.server_started = True
            
        if not test_instance:
            return

        from selenium import FIREFOX
        browser = connect(getattr(settings, "SELENIUM_BROWSER", FIREFOX))
        import pdb; pdb.set_trace()
        #          getattr(settings, "SELENIUM_HOST", 'localhost'),
        #          int(getattr(settings, "SELENIUM_PORT", 4444)),
        #          getattr(settings, "SELENIUM_BROWSER_COMMAND", '*opera'),
        #          getattr(settings, "SELENIUM_URL_ROOT", get_live_server_path()),
        #      )
        # clear test client for test isolation
        test_instance.browser = browser

    def stopTest(self, test):
        test_instance = get_test_case_instance(test)
        if getattr(test_instance, "browser", None):
            test_instance.browser.close()

    def finalize(self, result):
        self.stop_server()
