#!/usr/bin/env python3

"""Pure Python command-line RSS reader.

This program:

    - downloads information from RSS news feed
    - processes various data from news items (title, description, date, image, link)
    - prints data to console in text or JSON format
    - stores downloaded data to local cache file in SQL format
    - retrieves information from cache for a particular date
    - converts data to HTML and PDF formats and saves it to a local file

It supports all news feeds that fully comply with RSS 2.0 Specification.
Correct operation on other RSS channels is not guaranteed.

Most of the program has been written using Python's 3.9 standard library.
In order to convert news to PDF format xhtml2pdf module should be installed.
If current program is installed through a Wheel file or a Source Distribution file,
xhtml2pdf module is installed automatically. Otherwise you have to install it with its dependencies:
    Windows: py -m pip install xhtml2pdf
    Unix/MacOS: python3 -m pip install xhtml2pdf

Usage:

    Without installation:

        Windows:

            rss_reader.py <arguments>
            (run from directory with rss_reader.py)

            py -m rss_reader <arguments>
            (if directory with rss_reader.py is in sys.path)

        Unix/MacOS:

            python3 rss_reader.py <arguments>
            (run from directory with rss_reader.py)

            python3 -m rss_reader <arguments>
            (if directory with rss_reader.py is in sys.path)

    With installation of CLI utility:

        Windows/Unix/MacOS:

            rss_reader <arguments>

    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit]
    [--date] [--clean] [--to-html] [--to-pdf] [source]

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help  show this help message and exit
      --version   Print version info
      --json      Print result as JSON in stdout
      --verbose   Outputs verbose status messages
      --limit     Limit news topics if this parameter provided
      --date      Date formatted as YYYYMMDD
      --clean     Clean all data from cache file
      --to-html   Convert news to HTML format (provide path to folder or file *.html)
      --to-pdf    Convert news to PDF format (provide path to folder or file *.pdf)

Package structure:

    css - CSS files::

        arial.ttf
        Font with Cyrillic language support.

        css_html.css
        CSS file for HTML pages.

        css_pdf.css
        CSS file for PDF files.

    files - Various files:

        rss_cache.db
        SQL database.

        rss_man.png
        Callback image for xhtml2pdf module.

    tests - Supbackage for testing:

        __init__.py
        Subpackage initialization file.

        test_sql.db
        Test file with SQL database.

        tests.py
        Tests for RSS reader.

    __init__.py
    Package initialization file.

    __main__.py
    Allow program to run by package name.

    app.py
    Main program logic.

    rss_reader_config.py
    Parse arguments from command line and config logging.

    rss_reader_dates.py
    Parse and reformat dates.

    rss_reader_files.py
    Sanitize paths, convert to HTML string, create HTML and/or PDF files.

    rss_reader_sql.py
    SQL cache functionality (create table, store and retrieve data, clean cache).

    rss_reader_text.py
    String processing for command-line RSS reader.

    rss_reader_xml.py
    Download and process XML data.

Functions:

    run()
    Main program logic of RSS reader.
"""

import logging
import os.path

from .rss_reader_config import parse_args, config_logging
from .rss_reader_files import sanitize_paths, convert_to_html, create_files
from .rss_reader_text import dict_to_string
from .rss_reader_xml import download_xml, process_rss
from .rss_reader_sql import CACHE_FILE, create_sql_table, store_to_sql, retrieve_from_sql, clean_cache


def run():
    """Main program logic of RSS reader:
        - parse arguments from command-line input
        - config logging object to log events to stdout
        - create SQL table to hold downloaded RSS news items
        - download XML data from URL and process it
        - print data to console in text or JSON format
        - store and retrieve information from SQL table
        - clean SQL table
        - convert information to HTML and/or PDF formats
    """
    args = parse_args()
    arg_source = args["source"]
    arg_limit = args["limit"]
    arg_date = args["date"]
    config_logging(args["verbose"])
    logging.info(f"Input arguments: {args}")
    if not os.path.exists(CACHE_FILE):
        if not create_sql_table():
            return None
    if args["clean"]:
        clean_cache()
        return None
    elif arg_date is not None:
        news_dict = retrieve_from_sql(arg_date, arg_source, arg_limit)
        if news_dict is None:
            return None
    else:
        root = download_xml(arg_source)
        if root is None:
            return None
        news_dict = process_rss(arg_source, root, arg_limit)
        if news_dict is None:
            return None
        store_to_sql(news_dict)
    string_to_print = dict_to_string(news_dict, args["json"], arg_date, arg_source)
    logging.info("Printing information to stdout")
    print(string_to_print)
    if args["to_html"] is not None or args["to_pdf"] is not None:
        paths = {k: v for k, v in args.items() if k.startswith("to_") and v is not None}
        filenames = sanitize_paths(paths)
        if filenames:
            html_str = convert_to_html(news_dict, arg_date, arg_source)
            create_files(html_str, filenames)
    logging.info("Program finished")
