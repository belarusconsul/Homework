#!/usr/bin/env python3

"""Parse and reformat dates.

    Functions:

        parse_date(date: str, title: str) -> object
        Get datetime.datetime object from a string.

        reformat_date(date: str) -> str
        Reformat string with date from '%Y%m%d' to '%B %d, %Y'.
"""

import logging
from datetime import datetime


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


def reformat_date(date):
    "Reformat string with date from '%Y%m%d' to '%B %d, %Y'."
    date_as_date = datetime.strptime(date, "%Y%m%d")
    date_reformatted = datetime.strftime(date_as_date, "%B %d, %Y")
    return date_reformatted
