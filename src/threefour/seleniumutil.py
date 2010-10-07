import tempfile
import ConfigParser

from threefour import config, save_config
from threefour.util import download_url_to

JAR_DOWNLOAD_URL = ('http://selenium.googlecode.com/files/'
    'selenium-server-standalone-2.0a5.jar')


def get_selenium(url=JAR_DOWNLOAD_URL):
    """
    If needed, will grab the Selenium 2 jar file from the Internet and save it
    locally.  It then updates the config file with the new location of the jar.
    """
    try:
        path = config.get('selenium', 'jar_filename')
        if os.path.isfile(path):
            # We've already fetched Selenium, and the config has been updated
            return
    except ConfigParser.Error:
        # Selenium has not been fetched and the config has not been updated
        pass

    path = download_url_to(url, tempfile.mkdtemp())

    try:
        config.add_section('selenium')
    except ConfigParser.DuplicateSectionError:
        # We already have the section, that's ok
        pass

    config.set('selenium', 'jar_filename', path)

    save_config(config)
