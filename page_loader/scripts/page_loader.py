#!/usr/bin/env python3.10

"""Page Loader Main Script."""


import argparse
import sys

import requests
from page_loader.download import DEFAULT_DST_FOLDER, download

DESCRIPTION = 'Page Loader'
HELP_MESSAGE = 'output dir (default: "{0}")'.format(DEFAULT_DST_FOLDER)
SUCCESS_MESSAGE = "Page was successfully download into '{0}'"


def main():
    """Run Page Loader."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('url')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP_MESSAGE,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()

    try:
        page_path = download(args.url, args.output)
    except requests.exceptions.HTTPError as e:
        print('Failed to connect to server{0}, code {1} was returned {2}'
              .format(e.request.url, type(e).__name__, str(e)))
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print('Failed to load from {0}, error happens {1}:{2}'
              .format(e.request.url, type(e).__name__, str(e)))
        sys.exit(1)
    except OSError as e:
        print('Failed to save file, error happens. {0}:{1}'
              .format(type(e).__name__, str(e)))
        sys.exit(1)
    except BaseException as e:
        print('Unexpected error happens. {0}:{1}'
              .format(type(e).__name__, str(e)))
        sys.exit(1)

    print(SUCCESS_MESSAGE.format(page_path))


if __name__ == '__main__':
    main()
