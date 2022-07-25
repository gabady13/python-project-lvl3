"""Page-loader Parser Module."""

import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.common import make_filename, make_foldername

links = ['img', 'link', 'script']
links_attrs = {
    'img': 'src',
    'link': 'href',
    'script': 'src',
}


def is_equal(first_url, second_url):
    """Check local assets for local domain."""
    if first_url is None or second_url is None:
        return False

    first_url_parts = urlparse(first_url)
    second_url_parts = urlparse(second_url)

    return (
        second_url_parts.hostname is None
        or first_url_parts.hostname == second_url_parts.hostname
    )


def parse_page(page_data, url):
    """Parse html page."""
    html = BeautifulSoup(page_data, 'html.parser')
    assets = [
        asset
        for asset in html.find_all(links)
        if is_equal(url, asset.get(links_attrs[asset.name]))
    ]

    assets_urls = [
        urljoin(url, asset.get(links_attrs[asset.name])) for asset in assets
    ]

    for asset in assets:
        asset_name = make_filename(
            urljoin(url, asset.get(links_attrs[asset.name])),
        )
        asset[links_attrs[asset.name]] = os.path.join(
            make_foldername(url),
            asset_name,
        )

    return html.prettify(), assets_urls
