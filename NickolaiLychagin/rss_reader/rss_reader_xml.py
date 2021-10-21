#!/usr/bin/env python3

"""Download and process XML data.

    Functions:

        download_xml(url: str) -> object
        Download XML data from URL.

        process_rss(url: str, root: object, limit: int/None) -> dict
        Process XML data from RSS feed into a dictionary.
"""

import logging
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, urlunsplit, quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from .rss_reader_text import strip_text, get_absolute_url, get_image_link, get_ending


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
            logging.info(f"Non-ASCII URL converted to '{url}'")
        try:
            logging.info(f"Opening URL '{url}'")
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


def process_rss(url, root, limit):
    """Process XML data from RSS feed into a dictionary.

    Parameters
        url: str - URL of RSS channel.
        root: xml.etree.ElementTree.Element - XML document as a tree.
        limit: int/None - Number of news items to process. If None - process all items.

    Returns
        news_dict: dict - Dictionary of data from RSS channel.
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
            logging.info(f"Processing news item #{n}")
            title = item.find("title")
            title = "" if title is None or title.text is None else strip_text(title.text)
            logging.info(f"Title extracted: {title}")
            date = item.find("pubDate")
            date = "" if date is None or date.text is None else strip_text(date.text)
            logging.info(f"Date of publication extracted: {date}")
            desc = item.find("description")
            desc = "" if desc is None or desc.text is None else desc.text
            link = item.find("link")
            link = "" if link is None or link.text is None else strip_text(link.text)
            if link.startswith("/"):
                link = get_absolute_url(link, channel)
            logging.info(f"URL of the news item extracted: {link}")
            image = None
            enclosures = item.findall("enclosure")
            if enclosures:
                for enclosure in enclosures:
                    enc_type = enclosure.attrib.get("type", "")
                    if "image" in enc_type or not enc_type:
                        image = enclosure.attrib.get("url", None)
                        if image is not None and image:
                            break
            else:
                try:
                    image = get_image_link(desc)
                except IndexError:
                    for elem in list(item.iter()):
                        tag = elem.tag[elem.tag.find("}")+1:]
                        if tag in ["thumbnail", "content", "encoded"]:
                            image = elem.attrib.get("url", None)
                            if image is not None and image:
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
                        image = "https://www.rssboard.org/images/rss-man-graphic.png"
            if image.startswith("/"):
                image = get_absolute_url(image, channel)
            logging.info(f"URL of the news item's image extracted: {image}")
            desc = strip_text(desc)
            logging.info("Description extracted")
            news_dict[f"News {n}"] = {"Title": title,
                                      "Date": date,
                                      "Image": image,
                                      "Description": desc,
                                      "Link": link}
            logging.info(f"News item #{n} added to dictionary")
    channel_length = len(news_dict) - 1
    ending = get_ending(channel_length)
    if limit is not None and channel_length < limit:
        logging.warning(f"Limit set to {limit} but only {channel_length} news {ending} found")
    logging.info(f"{channel_length} news {ending} processed")
    return news_dict
