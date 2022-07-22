"""Common Module."""

import os
import re
from urllib.parse import urlparse


def make_filename(url):
    """Make name for assets."""
    url_parts = urlparse(url)
    name, extension = os.path.splitext(url_parts.path[1:])
    name = re.sub(r'\W', '-', os.path.join(url_parts.hostname, name))
    extension = extension if extension else '.html'
    return '{0}{1}'.format(name, extension)


def make_foldername(url: str):
    """Create folder name."""
    return make_filename(url).replace('.html', '_files')
