"""Logging module."""

import logging

logger = logging.getLogger(__name__)

format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
handler.setFormatter(format)

file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
file_handler = logging.FileHandler('page_loader.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(file_format)

logger.addHandler(handler)
logger.addHandler(file_handler)
