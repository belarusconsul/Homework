#!/usr/bin/env python3

"""SQL cache functionality (create table, store and retrieve data, clean cache).

    Constants:

        CACHE_FILE - Path to local file with SQL database (in folder 'files').

    Functions:

        create_sql_table() -> bool
        Create SQL table to hold downloaded RSS news items.

        store_to_sql(news_dict: dict)
        Store information from a dictionary to SQL table.

        retrieve_from_sql(date: str, source: str, limit: int/None) -> dict
        Retrieve information from SQL table to a dictionary.

        clean_cache(colorize: bool):
        Delete all data from SQL table and vacuum it.
"""

import logging
import os
import sqlite3

from .rss_reader_dates import parse_date, reformat_date
from .rss_reader_text import get_ending
from .rss_reader_colors import COLORS


# Path to local file with SQL database (in folder 'files')
CACHE_FILE = os.path.join(os.path.dirname(__file__), "files", "rss_cache.db")


def create_sql_table():
    """Create SQL table to hold downloaded RSS news items.

    Returns:
        bool - True if SQL table created or False otherwise.
    """

    try:
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
                    "link TEXT UNIQUE);")
        con.close()
        logging.info("SQL table for storing RSS news items created")
        return True
    except sqlite3.OperationalError:
        logging.error(f"Unable to create сache file '{CACHE_FILE}'")
        return False


def store_to_sql(news_dict):
    """Store information from a dictionary to SQL table.

    Parameters:
        news_dict: dict - Dictionary of data from RSS channel.
    """

    try:
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
                    cur.execute("UPDATE news SET "
                                "title = ?,"
                                "date = ?,"
                                "date_as_date = ?,"
                                "desc = ?,"
                                "image = ? WHERE "
                                "link == ? AND ("
                                "title <> ? OR "
                                "date <> ? OR "
                                "desc <> ? OR "
                                "image <> ?)",
                                (title, date, date_as_date, desc, image, link,
                                 title, date, desc, image))
        con.commit()
        changes = con.total_changes
        con.close()
        ending = get_ending(changes)
        existing = len(news_dict) - 1 - changes
        if existing:
            ending_existing = get_ending(existing)
            logging.info(f"{changes} news {ending} saved to cache. {existing} news {ending_existing} already in cache.")
        else:
            logging.info(f"{changes} news {ending} saved to cache.")
    except sqlite3.OperationalError as err:
        logging.error(f"Unable to store info to сache file '{CACHE_FILE}' - {err}")


def retrieve_from_sql(date, source, limit):
    """Retrieve information from SQL table to a dictionary.

    Parameters:
        date: str - Date as a string.
        source: str - URL of RSS channel.
        limit: int/None - Number of news items to process. If None - process all items.

    Returns
        news_dict: dict - Dictionary of data from SQL table.
    """

    try:
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
        logging.info("Starting retrieval of data from cache file")
        for row in cur:
            n += 1
            logging.info(f"Processing news item #{n}")
            news_dict[f"News {n}"] = {"Title": row[3],
                                      "Channel": row[1],
                                      "Channel URL": row[2],
                                      "Date": row[4],
                                      "Image": row[7],
                                      "Description": row[6],
                                      "Link": row[8]}
            logging.info(f"News item #{n} added to dictionary")
        con.close()
        dict_length = len(news_dict)
        ending = get_ending(dict_length)
        if news_dict:
            if limit is not None and dict_length < limit:
                logging.warning(f"Limit set to {limit} but only {dict_length} news {ending} found in cache")
            logging.info(f"{dict_length} news {ending} retrieved from cache")
            return news_dict
        else:
            date_reformatted = reformat_date(date)
            logging.error(f"No information found in cache for {date_reformatted}")
            return None
    except sqlite3.OperationalError as err:
        logging.error(f"Unable to retrieve info from сache file '{CACHE_FILE}' - {err}")


def clean_cache(colorize):
    """Delete all data from SQL table and vacuum it.

    Parameters:
        colorize: bool - True (print messages in colorized mode) or False (print messages in normal mode).
    """

    logging.warning(f"User requested to clean cache file '{CACHE_FILE}'")
    confirmation = ("Are you sure you want to clean all data from cache file? "
                    "Press 'y' to confirm or any other key to cancel.\n")
    if colorize:
        os.system("")
        consent = input(COLORS["red"] + confirmation + COLORS["reset"])
    else:
        consent = input(confirmation)
    if consent.upper() == "Y":
        try:
            con = sqlite3.connect(CACHE_FILE)
            cur = con.cursor()
            cur.execute("DELETE FROM news;")
            con.commit()
            cur.execute("VACUUM;")
            con.close()
            logging.info(f"Cache file '{CACHE_FILE}' cleaned of all data")
            message = "All data from cache file cleaned successfully"
            if colorize:
                print(COLORS["green"] + message + COLORS["reset"])
            else:
                print(message)
        except sqlite3.OperationalError as err:
            logging.error(f"Unable to clean сache file '{CACHE_FILE}' - {err}")
    else:
        logging.warning(f"Operation to clean cache file '{CACHE_FILE}' cancelled by user")
        message = "Operation cancelled"
        if colorize:
            print(COLORS["yellow"] + message + COLORS["reset"])
        else:
            print(message)
