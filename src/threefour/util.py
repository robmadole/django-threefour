import os


def download_url_to(url, saveto):
    """
    Downloads a url to a given directory in the filesystem
    """
    # make sure that we have a directory to save to
    if not os.path.isdir(saveto):
        raise IOError('Path %s is not a directory' % saveto)
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    saveto = os.path.join(saveto, os.path.basename(url))
    src = dst = None
    if not os.path.exists(saveto):  # Avoid repeated downloads
        try:
            src = urlopen(url)
            # Read/write all in one block, so we don't create a corrupt file
            # if the download is interrupted.
            data = src.read()
            dst = open(saveto, "wb")
            dst.write(data)
        finally:
            if src:
                src.close()
            if dst:
                dst.close()
    return os.path.realpath(saveto)
