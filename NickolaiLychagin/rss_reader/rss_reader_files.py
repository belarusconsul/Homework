#!/usr/bin/env python3

"""Sanitize paths, convert to HTML string, create HTML and/or PDF files.

    Functions:

        sanitize_paths(paths: dict) -> dict
        Check that path is valid and file creatable, create necessary folders,
        add file extension if absent, ask user to confirm file overwriting if it exists.

        convert_to_html(news_dict: dict, date: str/None, souce: str/None) -> str
        Convert information from a dictionary to HTML-formatted string.

        create_files(html_str: str, filenames: dict)
        Create HTML and/or PDF file from HTML-formatted string.
"""

import logging
import os
import sys
from datetime import datetime
from io import StringIO
from socket import gaierror
from xhtml2pdf import pisa

from .rss_reader_dates import parse_date, reformat_date


def sanitize_paths(paths):
    """Check that path is valid and file creatable, create necessary folders,
    add file extension if absent, ask user to confirm file overwriting if it exists.

    Parameters:
        paths: dict - Dictionary of formats and paths entered by user as input arguments.

    Returns
        filenames: dict - Dictionary of formats and valid paths.
    """

    filenames = {}
    for path in paths:
        filename = os.path.abspath(paths[path])
        file_extension = path[3:]
        if not filename.endswith(f".{file_extension}"):
            filename = os.path.join(filename, f"rss.{file_extension}")
        logging.info(f"Absolute path of {file_extension.upper()} file: {filename}")
        dirname = os.path.dirname(filename)
        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
                logging.info("Necessary new folder structure created")
            with open(filename, "r"):
                consent = input(f"File '{filename}' already exists. Do you want to overwrite it? "
                                "Press 'y' to confirm or any other key to cancel.\n")
                if consent.upper() == "Y":
                    filenames[path] = filename
                    logging.info(f"Consent received to rewrite the file {filename}")
        except FileNotFoundError:
            try:
                with open(filename, "x"):
                    filenames[path] = filename
            except PermissionError:
                logging.error(f"File {filename} can't be created: no permission")
            except Exception as err:
                logging.error(f"File {filename} can't be created: {err}")
        except PermissionError:
            logging.error(f"File {filename} can't be created: no permission")
        except OSError:
            logging.error(f"File {filename} can't be created: invalid path")
        except Exception as err:
            logging.error(f"File {filename} can't be created: {err}")
    return filenames


def convert_to_html(news_dict, date, source):
    """Convert information from a dictionary to HTML-formatted string.

    Parameters:
        news_dict: dict - Dictionary of data from RSS channel.
        date: str/None - Date of items retrieved from cache. None - indicates that items were downloaded from URL.
        souce: str/None - URL address of channel. None - indicates that items were downloaded from cache.

    Returns
        html_str: str - HTML-formatted string.
    """

    if date is not None:
        date_reformatted = reformat_date(date)
        if source is None:
            page_title = f"RSS news for {date_reformatted} from all channels"
            heading = f"<h1>{page_title}</h1>"
        else:
            page_title = f"RSS news for {date_reformatted} from channel {news_dict['News 1']['Channel']}"
            heading = (f"<h1>RSS news for {date_reformatted}<br>from channel "
                       f"<a href='{news_dict['News 1']['Channel URL']}' target='_blank'>"
                       f"{news_dict['News 1']['Channel']}</a></h1>")
    else:
        channel_title = news_dict["Channel"]["Title"]
        channel_url = news_dict["Channel"]["URL"]
        if channel_title:
            page_title = f"RSS news from channel {channel_title}"
            heading = f"<h1>RSS news from channel <a href='{channel_url}' target='_blank'>{channel_title}</a></h1>"
        else:
            page_title = f"RSS news from channel {channel_url}"
            heading = f"<h1>RSS news from channel <a href='{channel_url}' target='_blank'>{channel_url}</a></h1>"
    css_html = os.path.join(os.path.dirname(__file__), "css", "css_html.css")
    font = os.path.join(os.path.dirname(__file__), "css", "arial.ttf")
    page_head = (f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>{page_title}</title>"
                 f"<link rel='stylesheet' href='{css_html}'>"
                 f"<style>@font-face {{font-family: Arial; src: url('{font}');}}</style></head>")
    string_obj = StringIO()
    string_obj.write("<body>")
    string_obj.write(heading)
    n = 0
    for item in news_dict:
        if item.startswith("News"):
            n += 1
            item_title = news_dict[item]["Title"]
            item_image = news_dict[item]["Image"]
            item_date = news_dict[item]["Date"]
            item_desc = news_dict[item]["Description"]
            item_link = news_dict[item]["Link"]
            string_obj.write("<div class='flex-container'>")
            string_obj.write("<div class='flex-child-image'>")
            string_obj.write(f"<img src='{item_image}' alt='{item_title}'>")
            string_obj.write("</div><div class='flex-child-text'>")
            if item_title:
                string_obj.write(f"<h3>{item_title}</h3>")
            if date is not None and source is None:
                channel_title = news_dict[item]["Channel"]
                channel_url = news_dict[item]["Channel URL"]
                if channel_title:
                    string_obj.write(f"<b>Channel:</b> <a href='{channel_url}' target='_blank'>{channel_title}</a><br>")
                else:
                    string_obj.write(f"<b>Channel:</b> <a href='{channel_url}' target='_blank'>{channel_url}</a><br>")
            date_as_date = parse_date(item_date, item_title)
            if date_as_date == datetime(1900, 1, 1, 0, 0):
                html_date = item_date
            else:
                html_date = datetime.strftime(date_as_date, "%B %d, %Y - %H:%M")
            string_obj.write(f"{html_date}<br>")
            if item_desc:
                string_obj.write(f"<br>{item_desc}")
            if item_link:
                string_obj.write(f"<br><a href='{item_link}' target='_blank'>Read more</a>")
            string_obj.write("</div></div>")
    string_obj.write("</body></html>")
    page_body = string_obj.getvalue()
    html_str = page_head + page_body
    logging.info("Information converted to HTML format")
    return html_str


def create_files(html_str, filenames):
    """Create HTML and/or PDF file from HTML-formatted string.

    Parameters:
        html_str: str - HTML-formatted string.
        filenames: dict - Dictionary of formats and valid paths.
    """

    for filename in filenames:
        if filename == "to_html":
            with open(filenames[filename], "w", encoding="utf-8") as file:
                file.write(html_str)
                logging.info(f"HTML file '{filenames[filename]}' created.")
                print(f"File '{filenames[filename]}' successfully created.")
        else:
            try:
                pdf_file = open(filenames[filename], "w+b")
                css_pdf = os.path.join(os.path.dirname(__file__), "css", "css_pdf.css")
                with open(css_pdf, "r", encoding="utf-8") as f:
                    css_str = f.read()
            except PermissionError:
                logging.error(f"File {filenames[filename]} can't be opened: no permission")
            else:
                try:
                    pisa.CreatePDF(html_str, dest=pdf_file, encoding="utf-8", default_css=css_str)
                    logging.info(f"PDF file '{filenames[filename]}' created.")
                    print(f"File '{filenames[filename]}' successfully created.")
                # if no internet connection
                except gaierror:
                    logging.info("No internet connection. Building file with no photos")
                    font = os.path.join(os.path.dirname(__file__), "css", "arial.ttf")
                    image = os.path.join(os.path.dirname(__file__), "files", "rss_man.png")
                    # don't print excessive info messages
                    sys.stdout = None
                    pisa.CreatePDF(html_str, dest=pdf_file, encoding="utf-8", default_css=css_str,
                                   link_callback=lambda x, y: font if x.endswith("arial.ttf") else image)
                    sys.stdout = sys.__stdout__
                    logging.info(f"PDF file '{filenames[filename]}' created.")
                    print(f"File '{filenames[filename]}' successfully created.")
                # for possible other exceptions in xhtml2pdf module
                except Exception as err:
                    logging.error(f"File {filenames[filename]} can't be created: {err}")
                finally:
                    pdf_file.close()
