#!/usr/bin/env python3

"""String processing for command-line RSS reader.

    Functions:

        strip_text(text: str) -> str
        Remove HTML tags, HTML entities, spaces at the beginning and at the end of a string,
        excessive whitespace characters. Limit string to no more than 1000 characters.

        get_image_link(text: str) -> str
        Get image's URL from text with img tag.

        get_absolute_url(url: str, channel: object) -> str
        Get absolute URL from relative URL and protocol and domain name extracted from RSS channel.

        get_ending(num: int) -> str
        Return correct singular or plural form of the word 'item'.

        dict_to_string(news_dict: dict, json_flag: bool, date: str/None, souce: str/None) -> str
        Convert a dictionary of RSS data into a string.
"""

import json
import logging
import re
from io import StringIO
from html import unescape

from .rss_reader_dates import reformat_date


def strip_text(text):
    """Remove HTML tags, HTML entities, spaces at the beginning and at the end of a string,
    excessive whitespace characters. Limit string to no more than 1000 characters.

    Parameters:
        text: str - A string of text.

    Returns
        stripped: str - A string stripped of HTML tags, HTML entities, spaces at the
                        beginning and at the end, excessive whitespace characters,
                        limited to no more than 1000 characters.
    """

    stripped = re.sub(r"<.+?>", "", text).strip()
    stripped = re.sub(r"\s{2,}|&nbsp;|\n", " ", stripped)
    stripped = unescape(stripped)
    if len(stripped) > 997:
        stripped = "".join([stripped[: 997], "..."])
    return stripped


def get_image_link(text):
    """Get image's URL from text with img tag.

    Parameters:
        text: str - A string of text containing img tag.

    Returns
        image_link: str - A string with image's URL.
    """

    img_tag = re.findall(r"<img.+?>", text)[0]
    image_link = re.findall(r"""src=["'](.*?)["']""", img_tag)[0]
    return image_link


def get_absolute_url(url, channel):
    """Get absolute URL from relative URL and protocol and domain name extracted from RSS channel.

    Parameters:
        url: str - A string with relative URL.
        channel: xml.etree.ElementTree.Element - RSS channel as a tree.

    Returns
        absolute_url: str - A string with absolute URL.
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


def dict_to_string(news_dict, json_flag, date, source):
    """Convert a dictionary of RSS data into a string.

    Parameters:
        news_dict: dict - Dictionary of data.
        json_flag: bool - True (convert to json string) or False (convert to text string).
        date: str/None - Date of items retrieved from cache. None - indicates that items were downloaded from URL.
        souce: str/None - URL address of RSS channel. None - indicates that items were downloaded from cache.

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
            date_reformatted = reformat_date(date)
            if source is None:
                string_obj.write(f"RSS news for {date_reformatted} from all channels\n")
            else:
                string_obj.write(f"RSS news for {date_reformatted} from channel '{news_dict['News 1']['Channel']}'\n")
        string_obj.write("\n")
        for item in news_dict:
            if item.startswith("News"):
                if news_dict[item]["Title"]:
                    string_obj.write(f"Title: {news_dict[item]['Title']}\n")
                if date is not None and source is None:
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
