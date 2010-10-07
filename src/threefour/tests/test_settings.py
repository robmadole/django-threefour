import unittest

from nose.plugins.attrib import attr
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from threefour.plugin import ServerPlugin


class TestSettings(unittest.TestCase):
    def setUp(self):
        self._old_database_settings = settings.DATABASES

    def tearDown(self):
        settings.DATABASES = self._old_database_settings

    def test_ok_with_sqlite(self):
        settings.DATABASES =  {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'default.db',
            },
            'secondary': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'secondary.db',
            }
        }

        sp = ServerPlugin()

        self.assertTrue(sp.check_database_multithread_compilant())

    def test_checks_in_memory_db(self):
        settings.DATABASES =  {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }

        sp = ServerPlugin()

        self.assertRaises(ImproperlyConfigured, sp.check_database_multithread_compilant)

    def test_checks_in_memory_db_test_name(self):
        settings.DATABASES =  {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'default.db',
                'TEST_NAME': ':memory:',
            }
        }

        sp = ServerPlugin()

        self.assertRaises(ImproperlyConfigured, sp.check_database_multithread_compilant)
