#!/usr/bin/env python3

"""Pure Python command-line RSS reader.

This module:

    - downloads information from RSS news feed
    - processes various data from news items (title, description, date, image, link)
    - prints data to console in text or JSON format
    - stores downloaded data to local cache file in SQL format

It supports all news feeds that fully comply with RSS 2.0 Specification.
Correct operation on other RSS channels is not guaranteed.

The program is written in Python 3.9 with it's standard library.
Installation of additional modules is not required.

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

    Example usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--clean] [source]

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided
      --date DATE    Date formatted as YYYYMMDD
      --clean        Clean all data from cache file

Imported modules:

    argparse
    html
    json
    logging
    os.path
    re
    sqlite3
    xml.etree.ElementTree as ET
    datetime from datetime
    StringIO from io
    urlsplit, urlunsplit, quote from urllib.parse
    urlopen, Request from urllib.request
    HTTPError, URLError from urllib.error

Constants:

    CACHE_FILE - local file with SQL database stored in the program's folder

Functions:

    parse_args() -> object
    Parse arguments from command-line input.

    config_logging(verbose_flag: bool)
    Config logging object to log events to stdout.

    download_xml(url: str) -> object
    Download XML data from URL.

    strip_text(text: str) -> str
    Remove HTML tags, HTML entities, spaces at the beginning and at the end of a string,
    excessive whitespace characters. Limit string to no more than 1000 characters.

    get_image_link(text: str) -> str
    Get image's URL from text with img tag.

    get_absolute_url(url: str, channel: object) -> str
    Get absolute URL from relative URL and protocol and domain name extracted from RSS channel.

    get_ending(num: int) -> str
    Return correct singular or plural form of the word "item"

    process_rss(url: str, root: object, limit: int/None) -> dict
    Process XML data from a RSS feed into a dictionary.

    dict_to_string(news_dict: dict, json_flag: bool, date: str/None) -> str
    Convert a dictionary of RSS data into a string.

    create_sql_table()
    Create SQL table to hold downloaded RSS news items.

    parse_date(date: str, title: str) -> object
    Get datetime.datetime object from a string.

    store_to_sql(news_dict: dict)
    Store information from a dictionary to SQL table.

    retrieve_from_sql(date: str, source: str, limit: int/None) -> dict
    Retrieve information from SQL table to a dictionary.

    clean_cache():
    Delete all data from SQL table and vacuum it.

    run_rss_reader()
    Main program logic of a RSS reader.
"""

import argparse
import html
import json
import logging
import os.path
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
from io import StringIO
from urllib.parse import urlsplit, urlunsplit, quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


# Local file with SQL database stored in the program's folder
CACHE_FILE = os.path.join(os.path.split(__file__)[0], "rss_cache.db")


def parse_args():
    """Parse arguments from command-line input.

    Returns:
        args: argparse.Namespace - Namespace object with a dictionary of input arguments.
    """

    parser = argparse.ArgumentParser(prog="rss_reader.py",
                                     description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="version", version="Version 1.2",
                        help="Print version info")
    parser.add_argument("--json", action="store_true",
                        help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="Outputs verbose status messages")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit news topics if this parameter provided")
    parser.add_argument("--date", default=None,
                        help="Date formatted as YYYYMMDD")
    parser.add_argument("--clean", action="store_true",
                        help="Clean all data from cache file")
    parser.add_argument("source", nargs="?", default=None,
                        help="RSS URL")
    args = parser.parse_args()
    if not any((args.source, args.date, args.clean)):
        parser.error("either source or --date or --clean argument must be provided")
    if args.limit is not None and args.limit < 1:
        parser.error("argument --limit must be greater than 0")
    if args.date:
        try:
            datetime.strptime(args.date, "%Y%m%d")
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


def download_xml(url):
    """Download XML data from URL.

    Parameters:
        url: str - URL address.

    Returns
        root: xml.etree.ElementTree.Element - XML document as a tree.
    """

    splitted = urlsplit(url)
    if not splitted.scheme:
        logging.error(f"Invalid URL '{url}': no scheme supplied. Perhaps you meant http://{url}")
    elif not splitted.netloc:
        logging.error(f"Invalid URL '{url}': no host supplied.")
    else:
        if not url.isascii():
            url = urlunsplit(part.encode("idna").decode("utf-8") if i == 1
                             else quote(part)
                             for i, part in enumerate(splitted))
        try:
            logging.info(f"Opening '{url}'")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
            with urlopen(Request(url, headers=headers)) as response:
                root = ET.fromstring(response.read())
                logging.info("XML root object created")
                return root
        except HTTPError as err:
            logging.error(f"Download of URL '{url}' failed with error {err.code} - {err.reason}")
        except URLError as err:
            logging.error(f"Unable to open URL '{url}' due to error - {err.reason}")
        except ET.ParseError:
            logging.error(f"URL '{url}' does not have valid XML data")


def strip_text(text):
    """Remove HTML tags, HTML entities, spaces at the beginning and at the end of a string,
    excessive whitespace characters. Limit string to no more than 1000 characters.

    Parameters:
        text: str - Any string of text.

    Returns
        stripped: str - String stripped of HTML tags, HTML entities, spaces at the
                        beginning and at the end, excessive whitespace characters,
                        limited to no more than 1000 characters.
    """

    stripped = re.sub(r"<.+?>", "", text).strip()
    stripped = re.sub(r"\s{2,}|&nbsp;|\n", " ", stripped)
    stripped = html.unescape(stripped)
    if len(stripped) > 997:
        stripped = "".join([stripped[: 997], "..."])
    return stripped


def get_image_link(text):
    """Get image's URL from text with img tag.

    Parameters:
        text: str - A string of text containing img tag.

    Returns
        image_link: str - String with image's URL.
    """

    img_tag = re.findall(r"<img.+?>", text)[0]
    image_link = re.findall(r"""src=["'](.*?)["']""", img_tag)[0]
    return image_link


def get_absolute_url(url, channel):
    """Get absolute URL from relative URL and protocol and domain name extracted from RSS channel.

    Parameters:
        url: str - Relative URL.
        channel: xml.etree.ElementTree.Element - RSS channel as a tree.

    Returns
        absolute_url: str - String with absolute URL.
    """

    try:
        site = channel.find("link").text
        if site.endswith("/"):
            site = site[:-1]
        absolute_url = site + url
    except AttributeError:
        absolute_url = url
    return absolute_url


def get_ending(num):
    """Return correct singular or plural form of the word 'item'"""
    return "item" if num == 1 else "items"


def process_rss(url, root, limit):
    """Process XML data from a RSS feed into a dictionary.

    Parameters
        url: str - URL of a RSS channel.
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
    title = "" if title is None or title.text is None else strip_text(title.text)
    logging.info(f"RSS channel '{title}' found")
    desc = channel.find("description")
    desc = "" if desc is None or desc.text is None else strip_text(desc.text)
    news_dict["Channel"] = {"Title": title, "Description": desc, "URL": url}
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
            title = "" if title is None or title.text is None else strip_text(title.text)
            date = item.find("pubDate")
            date = "" if date is None or date.text is None else strip_text(date.text)
            desc = item.find("description")
            desc = "" if desc is None or desc.text is None else desc.text
            link = item.find("link")
            link = "" if link is None or link.text is None else strip_text(link.text)
            if link.startswith("/"):
                link = get_absolute_url(link, channel)
            image = None
            enclosures = item.findall("enclosure")
            if enclosures:
                for enclosure in enclosures:
                    enc_type = enclosure.attrib.get("type", "")
                    if "image" in enc_type or not enc_type:
                        image = enclosure.attrib.get("url", None)
            else:
                try:
                    image = get_image_link(desc)
                except IndexError:
                    for elem in list(item.iter()):
                        tag = elem.tag[elem.tag.find("}")+1:]
                        if tag in ["thumbnail", "content", "encoded"]:
                            image = elem.attrib.get("url", None)
                            if image is not None:
                                break
                            else:
                                try:
                                    image = get_image_link(elem.text)
                                    break
                                except (IndexError, AttributeError, TypeError):
                                    continue
            if image is None or not image:
                try:
                    image = channel.find("image").find("url").text
                except AttributeError:
                    try:
                        image = root.find("image").find("url").text
                    except AttributeError:
                        image = ""
            if image.startswith("/"):
                image = get_absolute_url(image, channel)
            desc = strip_text(desc)
            news_dict[f"News {n}"] = {"Title": title,
                                      "Date": date,
                                      "Image": image,
                                      "Description": desc,
                                      "Link": link}
    channel_length = len(news_dict) - 1
    ending = get_ending(channel_length)
    if limit is not None and channel_length < limit:
        logging.warning(f"Limit set to {limit} but only {channel_length} news {ending} found")
    logging.info(f"{channel_length} news {ending} processed")
    return news_dict


def dict_to_string(news_dict, json_flag, date):
    """Convert a dictionary of RSS data into a string.

    Parameters:
        news_dict: dict - Dictionary of data.
        json_flag: bool - True (convert to json string) or False (convert to text string).
        date: str/None - Date of items retrieved from cache. None - indication that items were downloaded from URL.

    Returns:
        final_string: str - A string with information from a dictionary.
    """

    if json_flag:
        final_string = json.dumps(news_dict, ensure_ascii=False, indent=4)
        logging.info("Data converted to JSON string")
    else:
        string_obj = StringIO()
        string_obj.write("\n")
        if date is None:
            if news_dict["Channel"]["Title"]:
                string_obj.write(f"Feed: {news_dict['Channel']['Title']}\n")
            if news_dict["Channel"]["Description"]:
                string_obj.write(f"Description: {news_dict['Channel']['Description']}\n")
            if news_dict["Channel"]["URL"]:
                string_obj.write(f"URL: {news_dict['Channel']['URL']}\n")
        else:
            date_as_date = datetime.strptime(date, "%Y%m%d")
            date_formatted = datetime.strftime(date_as_date, "%B %d, %Y")
            string_obj.write(f"Cached news items for date '{date_formatted}'\n")
        string_obj.write("\n")
        for item in news_dict:
            if item.startswith("News"):
                if news_dict[item]["Title"]:
                    string_obj.write(f"Title: {news_dict[item]['Title']}\n")
                if date:
                    if news_dict[item]["Channel"]:
                        string_obj.write(f"Channel: {news_dict[item]['Channel']}\n")
                    if news_dict[item]["Channel URL"]:
                        string_obj.write(f"Channel URL: {news_dict[item]['Channel URL']}\n")
                if news_dict[item]["Date"]:
                    string_obj.write(f"Date: {news_dict[item]['Date']}\n")
                if news_dict[item]["Image"]:
                    string_obj.write(f"Image: {news_dict[item]['Image']}\n")
                if news_dict[item]["Description"]:
                    string_obj.write(f"Detail: {news_dict[item]['Description']}\n")
                if news_dict[item]["Link"]:
                    string_obj.write(f"Read more: {news_dict[item]['Link']}\n")
                string_obj.write("\n")
        final_string = string_obj.getvalue()[:-1]
        logging.info("Data converted to text string")
    return final_string


def create_sql_table():
    """Create SQL table to hold downloaded RSS news items."""
    con = sqlite3.connect(CACHE_FILE)
    cur = con.cursor()
    cur.execute("CREATE TABLE news ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "channel TEXT, "
                "url TEXT, "
                "title TEXT, "
                "date TEXT, "
                "date_as_date DATE, "
                "desc TEXT, "
                "image TEXT, "
                "link TEXT, "
                "UNIQUE(channel, url, title, date, desc, image, link));")
    con.close()
    logging.info("SQL table for storing RSS news items created")


def parse_date(date, title):
    """Get datetime.datetime object from a string.

    Parameters:
        date: str - Date as a string.
        title: str - Title of a news item.

    Returns:
        date_as_date: datetime.datetime - datetime.datetime object parsed from string.
    """

    date_as_date = None
    date_formats = ["datetime.strptime(date[5:25], '%d %b %Y %H:%M:%S')",
                    "datetime.strptime(date[5:23], '%d %b %y %H:%M:%S')",
                    "datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')",
                    "datetime.strptime(date, '%Y-%m-%d %H:%M:%S')",
                    "datetime.strptime(date[-24:-4], '%d %b %Y %H:%M:%S')"]
    for date_format in date_formats:
        try:
            date_as_date = eval(date_format)
            break
        except ValueError:
            continue
    if date_as_date is None:
        date_as_date = datetime(1900, 1, 1)
        logging.warning(f"No date provided or wrong date format in news '{title}'. Date set to '19000101'.")
    return date_as_date


def store_to_sql(news_dict):
    """Store information from a dictionary to SQL table.

    Parameters:
        news_dict: dict - Dictionary of data from a RSS channel.
    """

    con = sqlite3.connect(CACHE_FILE)
    cur = con.cursor()
    channel = news_dict["Channel"]["Title"]
    url = news_dict["Channel"]["URL"]
    for item in news_dict:
        if item.startswith("News"):
            title = news_dict[item]["Title"]
            date = news_dict[item]["Date"]
            date_as_date = parse_date(date, title)
            desc = news_dict[item]["Description"]
            image = news_dict[item]["Image"]
            link = news_dict[item]["Link"]
            try:
                cur.execute("INSERT INTO news(channel, url, title, date, date_as_date, desc, image, link) "
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                            (channel, url, title, date, date_as_date, desc, image, link))
            except sqlite3.IntegrityError:
                continue
    con.commit()
    changes = con.total_changes
    con.close()
    existing = len(news_dict) - 1 - changes
    ending = get_ending(changes)
    if existing:
        ending_exist = get_ending(existing)
        logging.info(f"{changes} news {ending} saved to cache. {existing} news {ending_exist} already in cache.")
    else:
        logging.info(f"{changes} news {ending} saved to cache.")


def retrieve_from_sql(date, source, limit):
    """Retrieve information from SQL table to a dictionary.

    Parameters:
        date: str - Date as a string.
        source: str - URL of a RSS channel.
        limit: int/None - Number of news items to process. None - to process all items.

    Returns
        news_dict: dict - Dictionary of data from SQL table.
    """

    source = "%" if source is None else source
    con = sqlite3.connect(CACHE_FILE)
    cur = con.cursor()
    if limit is not None:
        cur.execute("SELECT * FROM news WHERE url LIKE ? AND STRFTIME('%Y%m%d', date_as_date)=? "
                    "ORDER BY date_as_date DESC LIMIT ?;", (source, date, limit))
    else:
        cur.execute("SELECT * FROM news WHERE url LIKE ? AND STRFTIME('%Y%m%d', date_as_date)=? "
                    "ORDER BY date_as_date DESC;", (source, date))
    news_dict = {}
    n = 0
    for row in cur:
        n += 1
        news_dict[f"News {n}"] = {"Title": row[3],
                                  "Channel": row[1],
                                  "Channel URL": row[2],
                                  "Date": row[4],
                                  "Image": row[7],
                                  "Description": row[6],
                                  "Link": row[8]}
    con.close()
    dict_length = len(news_dict)
    ending = get_ending(dict_length)
    if news_dict:
        if limit is not None and dict_length < limit:
            logging.warning(f"Limit set to {limit} but only {dict_length} news {ending} found in cache")
        logging.info(f"{dict_length} news {ending} retrieved from cache")
    else:
        logging.error(f"No information found in cache for '{date}'")
    return news_dict


def clean_cache():
    """Delete all data from SQL table and vacuum it."""
    consent = input("Are you sure you want to clean all data from cache file? "
                    "Press 'y' to confirm or any other key to cancel.\n")
    if consent.upper() == "Y":
        con = sqlite3.connect(CACHE_FILE)
        cur = con.cursor()
        cur.execute("DELETE FROM news;")
        con.commit()
        cur.execute("VACUUM;")
        con.close()
        logging.info("SQL table cleaned of all data")
        print("All data from cache file cleaned successfully")


def run_rss_reader():
    """Main program logic of a RSS reader:
        - parse arguments from command-line input
        - config logging object to log events to stdout
        - create SQL table to hold downloaded RSS news items
        - download XML data from URL and process it
        - print data to console in text or JSON format
        - store and retrieve information from SQL table
        - clean SQL table
    """

    args = parse_args()
    config_logging(args.verbose)
    if not os.path.exists(CACHE_FILE):
        create_sql_table()
    if args.clean:
        clean_cache()
        return None
    elif args.date is not None:
        news_dict = retrieve_from_sql(args.date, args.source, args.limit)
        if not news_dict:
            return None
    else:
        root = download_xml(args.source)
        if root is None:
            return None
        news_dict = process_rss(args.source, root, args.limit)
        if news_dict is None:
            return None
        store_to_sql(news_dict)
    string_to_print = dict_to_string(news_dict, args.json, args.date)
    logging.info("Printing information to stdout")
    print(string_to_print)
    logging.info("Program finished successfully")


if __name__ == "__main__":
    run_rss_reader()
