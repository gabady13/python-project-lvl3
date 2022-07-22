"""Page_loader parse."""

import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.common import make_filename, make_foldername

links = ['img', 'link', 'script']
link_attr = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def is_equal_host(first_url, second_url):
    """Check local assets for local domain."""
    url_first = urlparse(first_url)
    url_second = urlparse(second_url)

    return (url_second.hostname is
            None or url_first.hostname == url_second.hostname)


def parse_page(url, page_data):
    """Parse html page."""
    """Parse html file."""
    soup = BeautifulSoup(page_data, 'html.parser')
    assets = [
        asset
        for asset in soup.find_all(links)
        if is_equal_host(url, asset.get(link_attr[asset.name]))
    ]

    assets_urls = [asset.get(link_attr[asset.name]) for asset in assets]

    for asset in assets:
        asset_name = make_filename(
            urljoin(url, asset.get(link_attr[asset.name])),
        )
        asset[link_attr[asset.name]] = os.path.join(
            make_foldername(url),
            asset_name,
        )

    return soup.prettify(), assets_urls
