"""Page Loader Download Module."""

import os

import requests
from page_loader.common import make_filename
from page_loader.logger import get_logger, write_traceback
from page_loader.parser import parse_page
from progress.bar import IncrementalBar
from requests.exceptions import RequestException

DEFAULT_DST_FOLDER = os.getcwd()

logger = get_logger(__name__)


def get_resource(url, use_raise=True):
    """Download file."""
    try:
        req = requests.get(url)
        req.raise_for_status()
    except RequestException as exc:
        logger.warning('Resource "{0}" wasn\'t downloaded.'.format(url))
        logger.debug(exc, exc_info=True)
        if use_raise:
            raise

    return req.content


def save(file_content, dst, name):
    """Save downloaded content."""
    page_path = os.path.join(dst, name)

    mode = 'w' if isinstance(file_content, str) else 'wb'

    try:
        with open(page_path, mode) as filename:
            filename.write(file_content)
    except OSError as exc:
        logger.error(exc)
        write_traceback()
        raise

    return page_path


def download_assets(assets, dst):
    """Download page."""
    if not os.path.exists(dst):
        logger.info('Create "{0}" folder for assets.'.format(dst))

        os.mkdir(dst)

    with IncrementalBar(
        'Downloading:',
        max=len(assets),
        suffix='%(percent)d%%',
    ) as progress:
        for asset_url, asset_name in assets:
            asset_content = get_resource(asset_url, False)
            if not(asset_content is None):
                save(asset_content, dst, asset_name)
            progress.next()


def download(url, dst=DEFAULT_DST_FOLDER):
    """Download html page."""
    logger.info('Start download "{0}" to "{1}".'.format(url, dst))

    page_content = get_resource(url)
    html, assets_path, assets = parse_page(page_content, url)
    page_path = save(html, dst, make_filename(url))

    if assets:
        logger.info('Start download.')

        download_assets(assets, os.path.join(dst, assets_path))

    logger.info('Finish download "{0}".'.format(url))

    return page_path
