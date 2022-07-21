"""Page Loader Download Module."""

import os
import re
from typing import Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_DST_FOLDER = os.getcwd()

link_attr = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def has_attr(tag):
    """Check tag has attrs 'srx' or 'href'."""
    return tag.has_attr('src') or tag.has_attr('href')


def is_localdomain(outer_host: str, inner_host: str) -> bool:
    """Check local assets for local domain."""
    inner_parts = urlparse(inner_host)
    outer_parts = urlparse(outer_host)

    return (inner_parts.hostname is
            None or outer_parts.hostname == inner_parts.hostname)


def make_name(url) -> str:
    """Make name for assets."""
    url_parts = urlparse(url)
    name, extension = os.path.splitext(url_parts.path[1:])
    name = re.sub(r'\W', '-', os.path.join(url_parts.hostname, name))
    extension = extension if extension else '.html'
    return '{0}{1}'.format(name, extension)


def make_folder(url: str, dst: str) -> str:
    """Create folder for assets and return folder name."""
    filename, _ = os.path.splitext(make_name(url))
    foldername = '{0}{1}'.format(filename, '_files')
    os.mkdir(os.path.join(dst, foldername))

    return foldername


def download_assets(src: str, dst: str) -> None:
    """Download assets for page."""
    req = requests.get(src, stream=True)
    assert_name = make_name(src)

    with open(os.path.join(dst, assert_name), 'wb') as filename:
        filename.write(req.content)

    return assert_name


def parse_html(url: str, dst: str, html: str) -> Tuple:
    """Parse html file."""
    soup = BeautifulSoup(html, 'html.parser')
    assets = (
        asset
        for asset in soup.find_all(['img', 'link', 'script'])
        if is_localdomain(url, asset.get(link_attr[asset.name]))
    )

    if assets:
        assets_dst = make_folder(url, dst)
        for asset in assets:
            asset_name = download_assets(
                urljoin(url, asset.get(link_attr[asset.name])),
                os.path.join(dst, assets_dst))
            asset[link_attr[asset.name]] = os.path.join(assets_dst, asset_name)

    return soup.prettify()


def download(url: str, dst: str = DEFAULT_DST_FOLDER):
    """Download html page to dst folder."""
    request = requests.get(url, stream=True)
    html_name = make_name(url)
    html_data = parse_html(url, dst, request.text)

    with open(os.path.join(dst, html_name), 'w') as filename:
        filename.write(html_data)

    return os.path.join(dst, html_name)
