import os
import unittest
import tempfile
import ConfigParser

from nose.plugins.attrib import attr

from threefour.util import download_url_to
from threefour.seleniumutil import get_selenium, JAR_DOWNLOAD_URL

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


class TestGrabselenium(unittest.TestCase):
    def setUp(self):
        import threefour

        self._old_config = threefour.config
        self._old_rc_filename = threefour.RC_FILENAME
        threefour.RC_FILENAME = os.path.expanduser('~/.threefourrc_test')
        try:
            os.unlink(threefour.RC_FILENAME)
        except OSError:
            pass
        config = ConfigParser.ConfigParser()

    def tearDown(self):
        import threefour

        # Clean up temp directories
        try:
            os.unlink(os.path.dirname(
                threefour.config.get('selenium', 'jar_filename')))
        except (OSError, ConfigParser.Error):
            pass
        threefour.config = self._old_config
        threefour.RC_FILENAME = self._old_rc_filename

    def test_will_download_file(self):
        test_url = 'http://www.google.com/images/logos/ps_logo2.png'

        tempdir = tempfile.mkdtemp() 

        download_url_to(test_url, tempdir)

        self.assertTrue(os.path.isfile(os.path.join(
            tempdir, 'ps_logo2.png')))

    def test_selenium_available(self):
        """
        Make sure that the URL we have stored for the Selenium 2 jar is still
        valid
        """
        src = urlopen(JAR_DOWNLOAD_URL)

        first_byte = src.read(1024)

        self.assertEquals(1024, len(first_byte))

    def test_will_write_configuration_after_download(self):
        test_url = 'http://www.google.com/images/logos/ps_logo2.png'

        # Give it an alternative url for testing
        get_selenium(url=test_url)

        from threefour import config
        jar_filename = config.get('selenium', 'jar_filename')

        self.assertTrue(os.path.isfile(jar_filename))
        self.assertIn('ps_logo2.png', jar_filename)
