#!/usr/bin/env python3.10

import argparse

from page_loader.download import DEFAULT_DST_FOLDER, download

DESCRIPTION = 'Page Loader'
HELP = 'set output folder'


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('source')
    parser.add_argument(
        '-o',
        '--output',
        help=HELP,
        default=DEFAULT_DST_FOLDER,
    )

    args = parser.parse_args()
    download(args.source, args.output)


if __name__ == '__main__':
    main()
