import os
from ConfigParser import ConfigParser

# Setup the config object
RC_FILENAME = os.path.expanduser('~/.threefourrc')
config = ConfigParser()

if os.path.isfile(RC_FILENAME):
    with open(RC_FILENAME) as fh:
        config.read(fh)


def save_config(config):
    """
    Convienience method to save the configuration in the right spot
    """
    with open(RC_FILENAME, 'w') as fh:
        config.write(fh)
