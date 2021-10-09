#!/usr/bin/env python3

"""
Pure Python command-line RSS reader.

This module:

    - downloads information from RSS news feed
    - processes various data from news items (title, description, date, image, link)
    - prints data to console in text or JSON format

Usage:

    Without installation:

        Windows:

            rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
            (run from directory with rss_reader.py)

            py -m rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
            (if directory with rss_reader.py is in sys.path)

        Unix/MacOS:

            python3 rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
            (run from directory with rss_reader.py)

            python3 -m rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source
            (if directory with rss_reader.py is in sys.path)

    With installation of CLI utility:

        Windows/Unix/MacOS:

            rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided

Imported modules:

    argparse
    json
    logging
    re
    xml.etree.ElementTree
    StringIO from io
    urlparse from urllib.parse
    urlopen from urllib.request
    URLError, HTTPError from urllib.error

Functions:

    parse_args() -> object
    Parse arguments from command-line input.

    config_logging(verbose_flag: bool)
    Config logging object to log events to stdout.

    download_xml(url: str) -> object
    Download XML data from URL.

    strip_html(text: str) -> str
    Remove HTML tags and spaces at the beginning and at the end of a string.

    process_rss(root: object, limit: int/None) -> dict
    Process XML data from a RSS feed into a dictionary.

    dict_to_string(news_dict: dict, json_flag: bool) -> str
    Convert a dictionary of RSS data into a string.

    run_rss_reader()
    Main program logic of a RSS reader.
"""

import argparse
import json
import logging
import re
import xml.etree.ElementTree as ET
from io import StringIO
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def parse_args():
    """
    Parse arguments from command-line input.

    Returns:
        args: argparse.Namespace - Namespace object with a dictionary of arguments.
    """

    parser = argparse.ArgumentParser(prog="rss_reader.py",
                                     description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="version", version="Version 1.1",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit news topics if this parameter provided")
    parser.add_argument("source", help="RSS URL")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("argument --limit must be greater than 0")
    return args


def config_logging(verbose_flag):
    """
    Config logging object to log events to stdout.

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


def download_xml(url):
    """
    Download XML data from URL.

    Parameters:
        url: str - URL address.

    Returns
        root: xml.etree.ElementTree.Element - XML document as a tree.
    """

    url_parsed = urlparse(url)
    if not all([url_parsed.netloc, url_parsed.scheme]):
        logging.error(f"'{url}' does not seem to be a valid URL. Check that valid scheme is provided")
        return None
    try:
        logging.info(f"Opening '{url}'")
        with urlopen(url) as response:
            root = ET.fromstring(response.read())
            logging.info("XML root object created")
            return root
    except HTTPError as err:
        logging.error(f"Download of '{url}' failed with error {err.code} - {err.reason}")
    except URLError as err:
        logging.error(f"Unable to open '{url}' due to error - {err.reason}")
    except ET.ParseError:
        logging.error(f"'{url}' is not a valid XML")
    except UnicodeEncodeError:
        logging.error("Source URL must contain only latin characters")


def strip_html(text):
    """
    Remove HTML tags and spaces at the beginning and at the end of a string.

    Parameters:
        text: str - Any string of text.

    Returns
        str - String without HTML tags and spaces at the beginning and at the end.
    """

    return re.sub("<.+?>", "", text).strip()


def process_rss(root, limit):
    """
    Process XML data from a RSS feed into a dictionary.

    Parameters
        root: xml.etree.ElementTree.Element - XML document as a tree.
        limit: int/None - Number of news items to process. None - to process all items.

    Returns
        news_dict: dict - Dictionary of data from a RSS channel.
    """

    news_dict = {}
    channel = root.find("channel")
    if channel is None:
        logging.error("RSS channel was not found in XML document")
        return None
    title = channel.find("title")
    title = "" if title is None else strip_html(title.text)
    logging.info(f"RSS channel '{title}' found")
    desc = channel.find("description")
    desc = "" if desc is None else strip_html(desc.text)
    news_dict["Channel"] = {"Title": title, "Description": desc}
    if channel.find("item") is None:
        logging.error("No news found in RSS channel")
        return None
    n = 0
    for item in channel.iter("item"):
        if limit is not None and len(news_dict) > limit:
            break
        else:
            n += 1
            title = item.find("title")
            title = "" if title is None else strip_html(title.text)
            date = item.find("pubDate")
            date = "" if date is None else strip_html(date.text)
            image = item.find("enclosure")
            image = "" if image is None else strip_html(image.attrib.get("url", ""))
            desc = item.find("description")
            desc = "" if desc is None else strip_html(desc.text)
            link = item.find("link")
            link = "" if link is None else strip_html(link.text)
            news_dict[f"News {n}"] = {"Title": title,
                                      "Date": date,
                                      "Image": image,
                                      "Description": desc,
                                      "Link": link}
    channel_length = len(news_dict) - 1
    ending = "items" if channel_length > 1 else "item"
    if limit is not None and channel_length < limit:
        logging.warning(f"Limit set to {limit} but only {channel_length} news {ending} found")
    logging.info(f"{channel_length} news {ending} processed")
    return news_dict


def dict_to_string(news_dict, json_flag):
    """
    Convert a dictionary of RSS data into a string.

    Parameters:
        news_dict: dict - Dictionary of data from a RSS channel.
        json_flag: bool - True (convert to json string) or False (convert to text string).

    Returns:
        final_string: str - A string with information from a dictionary.
    """

    if json_flag:
        final_string = json.dumps(news_dict, ensure_ascii=False, indent=4)
        logging.info("Data converted to JSON string")
    else:
        string_obj = StringIO()
        string_obj.write(f"\nFeed: {news_dict['Channel']['Title']}\n")
        if news_dict["Channel"]["Description"]:
            string_obj.write(f"Description: {news_dict['Channel']['Description']}\n")
        string_obj.write("\n")
        for item in news_dict:
            if item.startswith("News"):
                if news_dict[item]["Title"]:
                    string_obj.write(f"Title: {news_dict[item]['Title']}\n")
                if news_dict[item]["Date"]:
                    string_obj.write(f"Date: {news_dict[item]['Date']}\n")
                if news_dict[item]["Image"]:
                    string_obj.write(f"Image: {news_dict[item]['Image']}\n")
                if news_dict[item]["Description"]:
                    string_obj.write(f"{news_dict[item]['Description']}\n")
                if news_dict[item]["Link"]:
                    string_obj.write(f"Read more: {news_dict[item]['Link']}\n")
                string_obj.write("\n")
        final_string = string_obj.getvalue()[:-1]
        logging.info("Data converted to text string")
    return final_string


def run_rss_reader():
    """
    Main program logic of a RSS reader:
        - parse arguments from command-line input
        - config logging object
        - download information from RSS news feed and process it
        - print data to console in text or JSON format
    """

    args = parse_args()
    config_logging(args.verbose)
    root = download_xml(args.source)
    if root is not None:
        news_dict = process_rss(root, args.limit)
        if news_dict is not None:
            string_to_print = dict_to_string(news_dict, args.json)
            logging.info("Printing information to stdout")
            print(string_to_print)
            logging.info("Program finished successfully")


if __name__ == "__main__":
    run_rss_reader()
