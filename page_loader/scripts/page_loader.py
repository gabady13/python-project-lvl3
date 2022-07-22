#!/usr/bin/env python3.10

"""Page Loader Main Script."""

import argparse
import sys

import page_loader.logger as logger
from page_loader.download import DEFAULT_DST_FOLDER, download

DESCRIPTION = 'Page Loader'
HELP = 'set output folder'


def main():
    """Run Page Loader script."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('source')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()

    try:
        download(args.source, args.output)
    except Exception as error:
        logger.logger.error(error)


if __name__ == '__main__':
    sys.exit(main())
