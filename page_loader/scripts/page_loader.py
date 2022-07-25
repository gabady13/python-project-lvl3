#!/usr/bin/env python3.10

"""Page Loader Main Script."""

import argparse
import sys

from page_loader.download import DEFAULT_DST_FOLDER, download
from requests.exceptions import RequestException

DESCRIPTION = 'Page Loader'
HELP_MESSAGE = 'set output folder'
END_MESSAGE = "Page was seccessfully download into '{0}'"


def main():
    """Run Page Loader script."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('source')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP_MESSAGE,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()

    try:
        page = download(args.source, args.output)
    except (Exception, RequestException) as exc:
        sys.exit(exc)

    print(END_MESSAGE.format(page))


if __name__ == '__main__':
    main()
