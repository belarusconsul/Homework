#!/usr/bin/env python3

"""Parse arguments from command line and config logging.

    Functions:

        parse_args() -> dict
        Parse arguments from command line.

        config_logging(verbose_flag: bool)
        Config logging object to log events to stdout.
"""

import argparse
import logging
from datetime import datetime


def parse_args():
    """Parse arguments from command line.

    Returns:
        args: dict - Dictionary of input arguments.
    """

    parser = argparse.ArgumentParser(prog="rss_reader.py",
                                     description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="version", version="Version 1.3",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None, metavar="",
                        help="Limit news topics if this parameter provided")
    parser.add_argument("--date", default=None, metavar="",
                        help="Date formatted as YYYYMMDD")
    parser.add_argument("--clean", action="store_true",
                        help="Clean all data from cache file")
    parser.add_argument("--to-html", default=None, metavar="",
                        help="Convert news to HTML file (provide path to folder or file *.html)")
    parser.add_argument("--to-pdf", default=None, metavar="",
                        help="Convert news to PDF file (provide path to folder or file *.pdf)")
    parser.add_argument("source", nargs="?", default=None,
                        help="RSS URL")
    args = vars(parser.parse_args())
    if not any((args["source"], args["date"], args["clean"])):
        parser.error("either source or --date or --clean argument must be provided")
    if args["limit"] is not None and args["limit"] < 1:
        parser.error("argument --limit must be greater than 0")
    if args["date"] is not None:
        try:
            datetime.strptime(args["date"], "%Y%m%d")
        except ValueError:
            parser.error("argument --date must be formatted as YYYYMMDD")
    return args


def config_logging(verbose_flag):
    """Config logging object to log events to stdout.

    Parameters:
        verbose_flag: bool - True (logging level DEBUG) or False (logging level ERROR).
    """

    if verbose_flag:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(levelname)s: %(asctime)s - %(message)s",
                            datefmt="%d.%m.%Y %H:%M:%S")
    else:
        logging.basicConfig(level=logging.ERROR,
                            format="%(levelname)s: %(message)s")
