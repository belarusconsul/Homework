#!/usr/bin/env python3

"""Parse arguments from command line and config logging.

    Functions:

        parse_args() -> dict
        Parse arguments from command line.

        config_logging(verbose: bool, colorize: bool)
        Config logging object to log events to stdout.

    Classes:

        MyFormatter(logging.Formatter)
        Custom logging.Formatter object
"""

import argparse
import logging
import os
import sys
from datetime import datetime

from .rss_reader_colors import COLORS


def parse_args():
    """Parse arguments from command line.

    Returns:
        args: dict - Dictionary of input arguments.
    """

    parser = argparse.ArgumentParser(prog="rss_reader.py",
                                     description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="version", version="Version 1.4",
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
    parser.add_argument("--colorize", action="store_true",
                        help="Print result in colorized mode")
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


def config_logging(verbose, colorize):
    """Config logging object to log events to stdout.

    Parameters:
        verbose: bool - True (logging level DEBUG) or False (logging level ERROR).
        colorize: bool - True (print messages in colorized mode) or False (print messages in normal mode).
    """

    if colorize:
        os.system("")
    handler = logging.StreamHandler(sys.stdout)
    formatter = MyFormatter(verbose, colorize)
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    if verbose:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.ERROR)


class MyFormatter(logging.Formatter):
    """Custom logging.Formatter object. Formats logging message depending on verbose level and colorize option"""

    format_debug = "%(levelname)s: %(asctime)s - %(message)s"
    format_error = "%(levelname)s: %(message)s"
    colorized_debug_info = COLORS["green"] + format_debug + COLORS["reset"]
    colorized_debug_warning = COLORS["yellow"] + format_debug + COLORS["reset"]
    colorized_debug_error = COLORS["red"] + format_debug + COLORS["reset"]
    colorized_error = COLORS["red"] + format_error + COLORS["reset"]

    def __init__(self, verbose, colorize):
        super().__init__(datefmt="%d.%m.%Y %H:%M:%S")
        self.verbose = verbose
        self.colorize = colorize

    def format(self, record):
        if self.verbose:
            if self.colorize:
                if record.levelno == logging.ERROR:
                    self._style._fmt = MyFormatter.colorized_debug_error
                elif record.levelno == logging.WARNING:
                    self._style._fmt = MyFormatter.colorized_debug_warning
                else:
                    self._style._fmt = MyFormatter.colorized_debug_info
            else:
                self._style._fmt = MyFormatter.format_debug
        else:
            if self.colorize:
                self._style._fmt = MyFormatter.colorized_error
            else:
                self._style._fmt = MyFormatter.format_error
        result = logging.Formatter.format(self, record)
        return result
