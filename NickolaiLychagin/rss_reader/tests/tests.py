#!/usr/bin/env python3

"""Tests for pure Python command-line RSS reader.

Usage:

    Windows:

        py -m unittest discover
        (run from directory with rss_reader.py)

    Unix/MacOS:

        python3 -m unittest discover
        (run from directory with rss_reader.py)

    If coverage module installed:

        coverage run -m unittest discover
        coverage report -m
        coverage html

Constants:

    TEST_FOLDER - Path to folder with test files.
    TEST_DB - Path to test file with SQL database.
    NEW_DB - Path to newly created test file with SQL database.
    NEW_FOLDER - Path to newly created test folder.
    TEST_HTML - Path to HTML test file.
    TEST_PDF - Path to PDF test file.
    TEST_INVALID_PATH - Invalid path.
    DEFAULT_CONNECT - Default socket.socket.connect method

Classes:

    TestParser(unittest.TestCase) - Tests for argparse functionality.

        Methods:

            test_parse_args
            Test to assert that command-line input is parsed correctly.

            test_required_arg
            Test to assert that situation with no required argument raises parser.error.

            test_limit_positive
            Test to assert that non-positive number as --limit argument raises parser.error.

            test_correct_date
            Test to assert that --date argument in wrong format raises parser.error.

    TestUrlErrors(unittest.TestCase) - Tests for catching errors while downloading and processing RSS data.

        Methods:

            test_no_scheme_error
            Test to assert that URL has scheme.

            test_no_host_error
            Test to assert that URL has host.

            test_non_ascii_url
            Test to assert that url is converted to ASCII character-set.

            test_url_error
            Test to assert that URLError is caught.

            test_http_error
            Test to assert that HTTPError is caught.

            test_etree_parse_error
            Test to assert that xml.etree.ElementTree.ParseError is caught.

            test_rss_channel_error
            Test to assert that situation with no 'channel' tag in XML is handled correctly.

            test_rss_item_error
            Test to assert that situation with no 'item' tag in XML is handled correctly.

    TestVerbose(unittest.TestCase) - Tests for logging functionality in verbose mode.

        Methods:

            test_log_info
            Test to assert that messages at INFO level are logged to stdout in verbose mode.

            test_log_warning
            Test to assert that messages at WARNING level are logged to stdout in verbose mode.

    TestDictionary(unittest.TestCase) - Tests for correct dictionary construction.

        Methods:

            test_dictionary_keys
            Test to assert that dictionary of RSS data has necessary keys.

            test_dictionary_length
            Test to assert that dictionary of RSS data is of correct length.

            test_image_url
            Test to assert that news item in dictionary has an image URL

    TestStringMethods(unittest.TestCase) - Tests for correct functionality of string processing.

        Methods:

            test_strip_text
            Test to assert that string is stripped of HTML tags, HTML entities,
            spaces at the beginning and at the end, excessive whitespace characters
            and limited to no more than 1000 characters.

            test_absolute_url
            Test to assert that absolute URL is received from relative URL and
            protocol and domain name extracted from RSS channel.

            test_dict_to_text_string
            Test to assert that dictionary is converted to text string correctly.

            test_dict_to_json_string
            Test to assert that dictionary is converted to JSON string correctly.

            test_cache_to_string
            Test to assert that information from cache is converted to string correctly.

    TestPrinting(unittest.TestCase) - Tests for printing to console functionality.

        Methods:

            tearDown
            Clean test file with SQL database.

            test_print_text_string
            Test to assert that text string is printed to console correctly.

            test_print_json_string
            Test to assert that JSON string is printed to console correctly.

    TestDatetime(unittest.TestCase) - Tests for correct datetime parsing.

        Methods:

            test_parse_date
            Test to assert that datetime.datetime object is parsed from string.

            test_reformat_date
            Test to assert that a string with date is reformatted from '%Y%m%d' to %B %d, %Y'

    TestSql(unittest.TestCase) - Tests for SQL functionality.

        Methods:

            setUp
            Clean test file with SQL database.

            tearDown
            Clean test file with SQL database.

            tearDownClass
            Delete newly created test file with SQL database.

            test_table_access
            Test to assert that sitution with no access to SQL table is handled correctly.

            test_create_table
            Test to assert that SQL table has been created.

            test_clean_table
            Test to assert that SQL table has been cleaned.

            test_store_to_table
            Test to assert that information has been stored to SQL table.

            test_retrieve_from_table_positive
            Test to assert that information is retrieved from SQL table correctly.

            test_retrieve_from_table_negative
            Test to assert that situation with no information in SQL table is handled correctly.

    TestPathFile(unittest.TestCase) - Tests for operations on paths and files.

        Methods:

            tearDown
            Delete test files and folders, restore socket.socket.connect method.

            test_path
            Test to assert that path is sanitized correctly.

            test_convert_to_html_cache
            Test to assert that converting to html from cache works correctly.

            test_convert_to_html_web
            Test to assert that converting to html from web works correctly.

            test_write_to_file
            Test to assert that HTML and PDF files are created.

            test_pdf_permission_error
            Test to assert that PermissionError in creating PDF file is handled correctly.

            test_pdf_no_internet_access
            Test to assert that PDF file is created without internet access.
"""

import argparse
import datetime
import os
import re
import socket
import sqlite3
import sys
import xml.etree.ElementTree as ET
import unittest
from io import StringIO
from shutil import rmtree
from unittest.mock import patch

from .. import app
from .. import rss_reader_config as rss_config
from .. import rss_reader_dates as rss_dates
from .. import rss_reader_files as rss_files
from .. import rss_reader_text as rss_text
from .. import rss_reader_xml as rss_xml
from .. import rss_reader_sql as rss_sql


# Path to folder with test files
TEST_FOLDER = os.path.split(__file__)[0]
# Path to test file with SQL database
TEST_DB = os.path.join(TEST_FOLDER, "test_sql.db")
# Path to newly created test file with SQL database
NEW_DB = os.path.join(TEST_FOLDER, "test_new_sql.db")
# Path to newly created test folder
NEW_FOLDER = os.path.join(TEST_FOLDER, "new_folder")
# Path to HTML test file
TEST_HTML = os.path.join(NEW_FOLDER, "rss.html")
# Path to PDF test file
TEST_PDF = os.path.join(NEW_FOLDER, "rss.pdf")
# Invalid path
TEST_INVALID_PATH = os.path.join(TEST_FOLDER, f"{'a'*1000}")
# Default socket.socket.connect method
DEFAULT_CONNECT = socket.socket.connect


class TestParser(unittest.TestCase):
    """Tests for argparse functionality.

    Methods:

        test_parse_args
        Test to assert that command-line input is parsed correctly.

        test_required_arg
        Test to assert that situation with no required argument raises parser.error.

        test_limit_positive
        Test to assert that non-positive number as --limit argument raises parser.error.

        test_correct_date
        Test to assert that --date argument in wrong format raises parser.error.
    """

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date="20211011",
                                           clean=False, limit=3, to_html=None,
                                           to_pdf="C://rss.pdf",
                                           source="https://news.yahoo.com/rss/"))
    def test_parse_args(self, mock_args):
        """Test to assert that command-line input is parsed correctly."""
        args = rss_config.parse_args()
        self.assertEqual(args["json"], False)
        self.assertEqual(args["verbose"], False)
        self.assertEqual(args["date"], "20211011")
        self.assertEqual(args["clean"], False)
        self.assertEqual(args["limit"], 3)
        self.assertIsNone(args["to_html"])
        self.assertEqual(args["to_pdf"], "C://rss.pdf")
        self.assertEqual(args["source"], "https://news.yahoo.com/rss/")

    @patch("sys.stderr", new_callable=StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=3, to_html=None, to_pdf=None,
                                           source=None))
    def test_required_arg(self, mock_args, mock_stderr):
        """Test to assert that situation with no required argument raises parser.error."""
        with self.assertRaises(SystemExit):
            rss_config.parse_args()

    @patch("sys.stderr", new_callable=StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=0, to_html=None, to_pdf=None,
                                           source="https://news.yahoo.com/rss/"))
    def test_limit_positive(self, mock_args, mock_stderr):
        """Test to assert that non-positive number as --limit argument raises parser.error."""
        with self.assertRaises(SystemExit):
            rss_config.parse_args()

    @patch("sys.stderr", new_callable=StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date="10112021",
                                           clean=False, limit=3, to_html=None, to_pdf=None,
                                           source=None))
    def test_correct_date(self, mock_args, mock_stderr):
        """Test to assert that --date argument in wrong format raises parser.error."""
        with self.assertRaises(SystemExit):
            rss_config.parse_args()


class TestUrlErrors(unittest.TestCase):
    """Tests for catching errors while downloading and processing RSS data.

    Methods:

        test_no_scheme_error
        Test to assert that URL has scheme.

        test_no_host_error
        Test to assert that URL has host.

        test_non_ascii_url
        Test to assert that url is converted to ASCII character-set.

        test_url_error
        Test to assert that URLError is caught.

        test_http_error
        Test to assert that HTTPError is caught.

        test_etree_parse_error
        Test to assert that xml.etree.ElementTree.ParseError is caught.

        test_rss_channel_error
        Test to assert that situation with no 'channel' tag in XML is handled correctly.

        test_rss_item_error
        Test to assert that situation with no 'item' tag in XML is handled correctly.
    """

    @patch("logging.error")
    def test_no_scheme_error(self, mock_log):
        """Test to assert that URL has scheme."""
        rss_xml.download_xml("google.com")
        message = "Invalid URL 'google.com': no scheme supplied. Perhaps you meant http://google.com"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    def test_no_host_error(self, mock_log):
        """Test to assert that URL has host."""
        rss_xml.download_xml("http://")
        message = "Invalid URL 'http://': no host supplied."
        mock_log.assert_called_with(message)

    @patch("logging.error")
    def test_non_ascii_url(self, mock_log):
        """Test to assert that url is converted to ASCII character-set."""
        rss_xml.download_xml("http://кто.рф")
        message = "URL 'http://xn--j1ail.xn--p1ai' does not have valid XML data"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    def test_url_error(self, mock_log):
        """Test to assert that URLError is caught."""
        rss_xml.download_xml("htt://google.com")
        message = "Unable to open URL 'htt://google.com' due to error - unknown url type: htt"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    def test_http_error(self, mock_log):
        """Test to assert that HTTPError is caught."""
        rss_xml.download_xml("https://google.com/aaa")
        message = "Download of URL 'https://google.com/aaa' failed with error 404 - Not Found"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://google.com"))
    def test_etree_parse_error(self, mock_args, mock_log):
        """Test to assert that xml.etree.ElementTree.ParseError is caught."""
        app.run()
        message = "URL 'https://google.com' does not have valid XML data"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://www.w3schools.com/xml/note.xml"))
    def test_rss_channel_error(self, mock_args, mock_log):
        """Test to assert that situation with no 'channel' tag in XML is handled correctly."""
        app.run()
        message = "RSS channel was not found in XML document"
        mock_log.assert_called_with(message)

    @patch("logging.error")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://florizel.by/feed"))
    def test_rss_item_error(self, mock_args, mock_log):
        """Test to assert that situation with no 'item' tag in XML is handled correctly."""
        app.run()
        message = "No news found in RSS channel"
        mock_log.assert_called_with(message)


class TestVerbose(unittest.TestCase):
    """Tests for logging functionality in verbose mode.

    Methods:

        test_log_info
        Test to assert that messages at INFO level are logged to stdout in verbose mode.

        test_log_warning
        Test to assert that messages at WARNING level are logged to stdout in verbose mode.
    """

    @patch("logging.info")
    def test_log_info(self, mock_log):
        """Test to assert that messages at INFO level are logged to stdout in verbose mode."""
        rss_xml.download_xml("https://news.yahoo.com/rss/")
        message = "XML root object created"
        mock_log.assert_called_with(message)

    @patch("logging.warning")
    def test_log_warning(self, mock_log):
        """Test to assert that messages at WARNING level are logged to stdout in verbose mode."""
        url = "https://www.independent.co.uk/news/uk/rss"
        root = rss_xml.download_xml(url)
        rss_xml.process_rss(url, root, 500)
        mock_log.assert_called_once()


class TestDictionary(unittest.TestCase):
    """Tests for correct dictionary construction.

    Methods:

        test_dictionary_keys
        Test to assert that dictionary of RSS data has necessary keys.

        test_dictionary_length
        Test to assert that dictionary of RSS data is of correct length.

        test_image_url
        Test to assert that news item in dictionary has an image URL
    """

    def test_dictionary_keys(self):
        """Test to assert that dictionary of RSS data has necessary keys."""
        url = "https://news.yahoo.com/rss/"
        root = rss_xml.download_xml(url)
        news_dict = rss_xml.process_rss(url, root, 3)
        for key in ["Channel", "News 1", "News 2", "News 3"]:
            self.assertIn(key, news_dict.keys())
        for key in ["Title", "Description", "URL"]:
            self.assertIn(key, news_dict["Channel"].keys())
        for key in ["Title", "Date", "Image", "Description", "Link"]:
            self.assertIn(key, news_dict["News 1"].keys())

    def test_dictionary_length(self):
        """Test to assert that dictionary of RSS data is of correct length."""
        url = "https://news.yahoo.com/rss/"
        root = rss_xml.download_xml(url)
        news_dict = rss_xml.process_rss(url, root, 4)
        self.assertEqual(len(news_dict), 5)

    def test_image_url(self):
        """Test to assert that news item in dictionary has an image URL"""
        url_1 = "https://lenta.ru/rss/news"
        root_1 = rss_xml.download_xml(url_1)
        news_dict_1 = rss_xml.process_rss(url_1, root_1, 1)
        url_2 = "https://www.independent.co.uk/news/uk/rss"
        root_2 = rss_xml.download_xml(url_2)
        news_dict_2 = rss_xml.process_rss(url_2, root_2, 1)
        url_3 = "https://news.mail.ru/rss/politics/91/"
        root_3 = rss_xml.download_xml(url_3)
        news_dict_3 = rss_xml.process_rss(url_3, root_3, 1)
        url_4 = "https://knife.media/feed/"
        root_4 = rss_xml.download_xml(url_4)
        news_dict_4 = rss_xml.process_rss(url_4, root_4, 10)
        image_4 = False
        for elem in news_dict_4:
            if elem.startswith("News"):
                if ".jp" in news_dict_4[elem]["Image"]:
                    image_4 = True
                    break
        url_5 = "https://pravo.by/novosti/obshchestvenno-politicheskie-i-v-oblasti-prava/rss/"
        root_5 = rss_xml.download_xml(url_5)
        news_dict_5 = rss_xml.process_rss(url_5, root_5, 10)
        image_5 = False
        for elem in news_dict_5:
            if elem.startswith("News"):
                if ".jp" in news_dict_5[elem]["Image"]:
                    image_5 = True
                    break
        self.assertIn("image", news_dict_1["News 1"]["Image"])
        self.assertIn("webp", news_dict_2["News 1"]["Image"])
        self.assertEqual("https://news.mail.ru/img/logo/news/news_web.png", news_dict_3["News 1"]["Image"])
        self.assertTrue(image_4)
        self.assertTrue(image_5)


class TestStringMethods(unittest.TestCase):
    """Tests for correct functionality of string processing.

    Methods:

        test_strip_text
        Test to assert that string is stripped of HTML tags, HTML entities,
        spaces at the beginning and at the end, excessive whitespace characters
        and limited to no more than 1000 characters.

        test_absolute_url
        Test to assert that absolute URL is received from relative URL and
        protocol and domain name extracted from RSS channel.

        test_dict_to_text_string
        Test to assert that dictionary is converted to text string correctly.

        test_dict_to_json_string
        Test to assert that dictionary is converted to JSON string correctly.

        test_cache_to_string
        Test to assert that information from cache is converted to string correctly.
    """

    def test_strip_text(self):
        """Test to assert that string is stripped of HTML tags, HTML entities,
        spaces at the beginning and at the end, excessive whitespace characters
        and limited to no more than 1000 characters.
        """

        test_text = """   <p>Python&nbsp;is an easy to learn, powerful programming language.
        It has efficient high-level data structures and a simple but
        effective approach to object-oriented programming.\nPython’s
        elegant syntax and dynamic typing, together with its
        interpreted nature, make it an ideal language for scripting
        and rapid application development in many areas on most
        platforms. The Python interpreter and the extensive
        standard library are freely available in source or
        binary form for all major platforms from the Python
        web&nbsp;site, https://www.python.org/, and may be
        freely distributed. The        same site also contains&lt;
        distributions of and pointers to many free third party Python modules,
        programs and tools, and additional documentation. The Python
        interpreter is easily extended with new functions and data
        types implemented in C or C++ (or other languages callable
                    from C). Python is also suitable as an extension
        language for customizable applications. This tutorial
        introduces the reader informally to the basic concepts
        and features of the Python language and system.<p>   """
        stripped_text = rss_text.strip_text(test_text)
        self.assertNotIn("<p>", stripped_text)
        self.assertNotIn("  ", stripped_text)
        self.assertNotIn("\n", stripped_text)
        self.assertNotIn("&nbsp;", stripped_text)
        self.assertIn("<", stripped_text)
        self.assertEqual(len(stripped_text), 1000)

    def test_absolute_url(self):
        """Test to assert that absolute URL is received from relative URL and
        protocol and domain name extracted from RSS channel.
        """
        url = "https://www.cbr.ru/scripts/RssCurrency.asp"
        root = rss_xml.download_xml(url)
        relative_url = root.find("channel").find("item").find("link").text
        news_dict = rss_xml.process_rss(url, root, 1)
        xml_string = "<rss><channel></channel></rss>"
        channel = ET.fromstring(xml_string).find("channel")
        negative_result = rss_text.get_absolute_url(relative_url, channel)
        self.assertTrue(relative_url.startswith("/"))
        self.assertTrue(news_dict["News 1"]["Link"].startswith("http://"))
        self.assertFalse(negative_result.startswith("http://"))

    def test_dict_to_text_string(self):
        """Test to assert that dictionary is converted to text string correctly."""
        test_dict = {"Channel": {"Title": "s0",
                                 "Description": "s1",
                                 "URL": "s2"},
                     "News 1": {"Title": "s3",
                                "Date": "s4",
                                "Image": "s5",
                                "Description": "s6",
                                "Link": "s7"}}
        test_string = rss_text.dict_to_string(test_dict, False, None, "s2")
        compare_string = "\nFeed: s0\nDescription: s1\nURL: s2\n\nTitle: s3\nDate: s4\nImage: s5\nDetail: s6\n"
        self.assertIn(compare_string, test_string)

    def test_dict_to_json_string(self):
        """Test to assert that dictionary is converted to JSON string correctly."""
        test_dict = {"Channel": {"Title": "Новости"}}
        test_string = rss_text.dict_to_string(test_dict, True, None, "s2")
        compare_string = '{\n    "Channel": {\n        "Title": "Новости"\n    }\n}'
        self.assertEqual(test_string, compare_string)

    def test_cache_to_string(self):
        """Test to assert that information from cache is converted to string correctly."""
        test_dict = {"News 1": {"Title": "s1",
                                "Channel": "s2",
                                "Channel URL": "s3",
                                "Date": "s4",
                                "Image": "s5",
                                "Description": "s6",
                                "Link": "s7"}}
        test_string = rss_text.dict_to_string(test_dict, False, "20211012", "s2")
        compare_string = "\nRSS news for October 12, 2021 from channel 's2'\n\nTitle: s1\n"
        self.assertIn(compare_string, test_string)


class TestPrinting(unittest.TestCase):
    """Tests for printing to console functionality.

    Methods:

        tearDown
        Clean test file with SQL database.

        test_print_text_string
        Test to assert that text string is printed to console correctly.

        test_print_json_string
        Test to assert that JSON string is printed to console correctly.
    """

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def tearDown(self, mock_input, mock_stdout):
        """Clean test file with SQL database."""
        rss_sql.clean_cache()

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://feeds.skynews.com/feeds/rss/home.xml"))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_print_text_string(self, mock_args):
        """Test to assert that text string is printed to console correctly."""
        captured_output = StringIO()
        sys.stdout = captured_output
        app.run()
        sys.stdout = sys.__stdout__
        captured_output.seek(1)
        self.assertIn("Sky News", captured_output.readline())
        self.assertIn("Description: ", captured_output.readline())
        self.assertIn("URL: ", captured_output.readline())
        captured_output.readline()
        self.assertIn("Title: ", captured_output.readline())
        self.assertIn("Date: ", captured_output.readline())
        self.assertIn("Image: ", captured_output.readline())
        self.assertIn("Detail: ", captured_output.readline())
        self.assertIn("Read more: ", captured_output.readline())

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=True, verbose=True, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://feeds.skynews.com/feeds/rss/home.xml"))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_print_json_string(self, mock_args):
        """Test to assert that JSON string is printed to console correctly."""
        captured_output = StringIO()
        sys.stdout = captured_output
        app.run()
        sys.stdout = sys.__stdout__
        captured_output.seek(2)
        self.assertIn('    "Channel": {\n', captured_output.readline())
        self.assertIn('        "Title"', captured_output.readline())
        self.assertIn('        "Description"', captured_output.readline())
        self.assertIn('        "URL"', captured_output.readline())
        captured_output.readline()
        self.assertIn('    "News 1": {\n', captured_output.readline())
        self.assertIn('        "Title"', captured_output.readline())
        self.assertIn('        "Date"', captured_output.readline())
        self.assertIn('        "Image"', captured_output.readline())
        self.assertIn('        "Description"', captured_output.readline())
        self.assertIn('        "Link"', captured_output.readline())


class TestDatetime(unittest.TestCase):
    """Tests for correct datetime parsing.

    Methods:

        test_parse_date
        Test to assert that datetime.datetime object is parsed from string.

        test_reformat_date
        Test to assert that a string with date is reformatted from '%Y%m%d' to %B %d, %Y'
    """

    @patch("sys.stderr", new_callable=StringIO)
    def test_parse_date(self, mock_stderr):
        """Test to assert that datetime.datetime object is parsed from string."""
        title = "Test news"
        date_1 = "Tue, 12 Oct 2021 17:06:02 +0300"
        date_as_date_1 = rss_dates.parse_date(date_1, title)
        date_2 = "Tue, 12 Oct 21 17:06:02 +0300"
        date_as_date_2 = rss_dates.parse_date(date_2, title)
        date_3 = "2021-10-12T17:06:02Z"
        date_as_date_3 = rss_dates.parse_date(date_3, title)
        date_4 = "2021-10-12 17:06:02"
        date_as_date_4 = rss_dates.parse_date(date_4, title)
        date_5 = "Tuesday, 12 Oct 2021 17:06:02 EST"
        date_as_date_5 = rss_dates.parse_date(date_5, title)
        date_6 = "12.10.2021"
        date_as_date_6 = rss_dates.parse_date(date_6, title)
        test_object_1 = datetime.datetime(2021, 10, 12, 17, 6, 2)
        test_object_2 = datetime.datetime(1900, 1, 1, 0, 0, 0)
        self.assertEqual(date_as_date_1, test_object_1)
        self.assertEqual(date_as_date_2, test_object_1)
        self.assertEqual(date_as_date_3, test_object_1)
        self.assertEqual(date_as_date_4, test_object_1)
        self.assertEqual(date_as_date_5, test_object_1)
        self.assertEqual(date_as_date_6, test_object_2)

    def test_reformat_date(self):
        """Test to assert that a string with date is reformatted from '%Y%m%d' to %B %d, %Y'"""
        test_date = "20211014"
        reformatted_date = rss_dates.reformat_date(test_date)
        self.assertEqual(reformatted_date, "October 14, 2021")


class TestSql(unittest.TestCase):
    """Tests for SQL functionality.

    Methods:

        setUp
        Clean test file with SQL database.

        tearDown
        Clean test file with SQL database.

        tearDownClass
        Delete newly created test file with SQL database.

        test_table_access
        Test to assert that sitution with no access to SQL table is handled correctly.

        test_create_table
        Test to assert that SQL table has been created.

        test_clean_table
        Test to assert that SQL table has been cleaned.

        test_store_to_table
        Test to assert that information has been stored to SQL table.

        test_retrieve_from_table_positive
        Test to assert that information is retrieved from SQL table correctly.

        test_retrieve_from_table_negative
        Test to assert that situation with no information in SQL table is handled correctly.
    """

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def setUp(self, mock_input, mock_stdout):
        """Clean test file with SQL database."""
        rss_sql.clean_cache()

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def tearDown(self, mock_input, mock_stdout):
        """Clean test file with SQL database."""
        rss_sql.clean_cache()

    @classmethod
    def tearDownClass(cls):
        """Delete newly created test file with SQL database."""
        if os.path.exists(NEW_DB):
            os.remove(NEW_DB)

    @patch("logging.error")
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=True, limit=1, to_html=None, to_pdf=None,
                                           source=None))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_INVALID_PATH)
    def test_table_access(self, mock_args, mock_input, mock_stdout, mock_log):
        """Test to assert that sitution with no access to SQL table is handled correctly."""
        rss_sql.create_sql_table()
        mock_log.assert_called_once()
        mock_log.reset_mock()
        rss_sql.store_to_sql({})
        mock_log.assert_called_once()
        mock_log.reset_mock()
        rss_sql.retrieve_from_sql("19011016", None, 1)
        mock_log.assert_called_once()
        mock_log.reset_mock()
        rss_sql.clean_cache()
        mock_log.assert_called_once()

    @patch("rss_reader.rss_reader_sql.CACHE_FILE", NEW_DB)
    def test_create_table(self):
        """Test to assert that SQL table has been created."""
        rss_sql.create_sql_table()
        self.assertTrue(os.path.exists(NEW_DB))

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=True, limit=None, to_html=None, to_pdf=None,
                                           source=None))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_clean_table(self, mock_args, mock_input, mock_stdout):
        """Test to assert that SQL table has been cleaned."""
        app.run()
        output = mock_stdout.getvalue()
        self.assertIn("All data from cache file cleaned successfully\n", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None, to_pdf=None,
                                           source="https://www.cbr.ru/scripts/RssCurrency.asp"))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_store_to_table(self, mock_args, mock_stdout):
        """Test to assert that information has been stored to SQL table."""
        app.run()
        con = sqlite3.connect(TEST_DB)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM news")
        result_1 = cur.fetchone()[0]
        con.close()
        app.run()
        con = sqlite3.connect(TEST_DB)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM news")
        result_2 = cur.fetchone()[0]
        con.close()
        self.assertEqual(result_1, 1)
        self.assertEqual(result_2, 1)

    @patch("logging.warning")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date="20211012",
                                           clean=False, limit=2, to_html=None, to_pdf=None,
                                           source=None))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_retrieve_from_table_positive(self, mock_args, mock_log):
        """Test to assert that information is retrieved from SQL table correctly."""
        title = "Test news"
        date = "Tue, 12 Oct 2021 21:16:42 +0300"
        date_as_date = rss_dates.parse_date(date, title)
        con = sqlite3.connect(TEST_DB)
        cur = con.cursor()
        cur.execute("INSERT INTO news(channel, url, title, date, date_as_date) "
                    "VALUES('s1', 's2', 's3', ?, ?);",
                    (date, date_as_date))
        con.commit()
        con.close()
        captured_output = StringIO()
        sys.stdout = captured_output
        app.run()
        sys.stdout = sys.__stdout__
        captured_output.seek(1)
        self.assertEqual("RSS news for October 12, 2021 from all channels\n", captured_output.readline())
        captured_output.readline()
        self.assertEqual("Title: s3\n", captured_output.readline())
        self.assertEqual("Channel: s1\n", captured_output.readline())
        self.assertEqual("Channel URL: s2\n", captured_output.readline())
        self.assertEqual("Date: Tue, 12 Oct 2021 21:16:42 +0300\n", captured_output.readline())
        mock_log.assert_called_once()

    @patch("logging.error")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date="20211011",
                                           clean=False, limit=None, to_html=None, to_pdf=None,
                                           source="https://news.yahoo.com/rss/"))
    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    def test_retrieve_from_table_negative(self, mock_args, mock_log):
        """Test to assert that situation with no information in SQL table is handled correctly."""
        title = "Test news"
        date = "Tue, 12 Oct 2021 21:16:42 +0300"
        date_as_date = rss_dates.parse_date(date, title)
        con = sqlite3.connect(TEST_DB)
        cur = con.cursor()
        cur.execute("INSERT INTO news(channel, url, title, date, date_as_date) "
                    "VALUES('s1', 's2', 's3', ?, ?);",
                    (date, date_as_date))
        con.commit()
        con.close()
        app.run()
        message = "No information found in cache for October 11, 2021"
        mock_log.assert_called_with(message)


class TestPathFile(unittest.TestCase):
    """Tests for operations on paths and files.

    Methods:

        tearDown
        Delete test files and folders, restore socket.socket.connect method.

        test_path
        Test to assert that path is sanitized correctly.

        test_convert_to_html_cache
        Test to assert that converting to html from cache works correctly.

        test_convert_to_html_web
        Test to assert that converting to html from web works correctly.

        test_write_to_file
        Test to assert that HTML and PDF files are created.

        test_pdf_permission_error
        Test to assert that PermissionError in creating PDF file is handled correctly.

        test_pdf_no_internet_access
        Test to assert that PDF file is created without internet access.
    """

    def tearDown(self):
        """Delete test files and folders, restore socket.socket.connect method."""
        for path in [TEST_HTML, TEST_PDF]:
            if os.path.exists(path):
                os.chmod(path, 0o777)
                os.remove(path)
        for path in [NEW_FOLDER, "C:\\Windows\\xxxyyyzzz\\"]:
            if os.path.exists(path):
                os.chmod(path, 0o777)
                rmtree(path)
        socket.socket.connect = DEFAULT_CONNECT

    @patch("logging.error")
    @patch("builtins.input", return_value="y")
    def test_path(self, mock_input, mock_log):
        """Test to assert that path is sanitized correctly."""
        paths = {"to_html": f"{NEW_FOLDER}"}
        filenames = rss_files.sanitize_paths(paths)
        self.assertEqual(filenames["to_html"], TEST_HTML)
        filenames = rss_files.sanitize_paths(paths)
        self.assertEqual(filenames["to_html"], TEST_HTML)
        paths = {"to_html": TEST_INVALID_PATH}
        rss_files.sanitize_paths(paths)
        mock_log.assert_called_once()
        mock_log.reset_mock()
        if os.name == "nt":
            paths = {"to_html": "C:\\Windows\\xxxyyyzzz.html"}
            rss_files.sanitize_paths(paths)
            mock_log.assert_called_once()
            mock_log.reset_mock()
            paths = {"to_html": "C:\\Windows\\xxxyyyzzz\\xxxyyyzzz.html"}
            rss_files.sanitize_paths(paths)
            mock_log.assert_called_once()
        elif os.name == "posix":
            if not os.path.exists(NEW_FOLDER):
                os.mkdir(NEW_FOLDER)
            os.chmod(NEW_FOLDER, 0o555)
            paths = {"to_html": os.path.join(NEW_FOLDER, "rss2.html")}
            rss_files.sanitize_paths(paths)
            mock_log.assert_called_once()
            mock_log.reset_mock()
            paths = {"to_html": os.path.join(NEW_FOLDER, "rss")}
            rss_files.sanitize_paths(paths)
            mock_log.assert_called_once()

    @patch("logging.warning")
    def test_convert_to_html_cache(self, mock_log):
        """Test to assert that converting to html from cache works correctly."""
        test_dict_1 = {"News 1": {"Title": "s0",
                                  "Channel": "s1",
                                  "Channel URL": "s2",
                                  "Date": "Mon, 18 Oct 2021 17:44:33 +0300",
                                  "Image": "https://www.rssboard.org/images/rss-man-graphic.png",
                                  "Description": "s5",
                                  "Link": "s6"}}
        test_dict_2 = {"News 1": {"Title": "s0",
                                  "Channel": "",
                                  "Channel URL": "s2",
                                  "Date": "18 Oct 2021",
                                  "Image": "s4",
                                  "Description": "s5",
                                  "Link": ""}}
        html_str_1 = rss_files.convert_to_html(test_dict_1, "20211018", "s2")
        html_str_2 = rss_files.convert_to_html(test_dict_2, "19000101", None)
        html_str_3 = rss_files.convert_to_html(test_dict_1, "20211018", None)
        page_title_1 = re.findall(r"<title>(.*?)</title>", html_str_1)[0]
        page_title_2 = re.findall(r"<title>(.*?)</title>", html_str_2)[0]
        image_src_1 = re.findall(r"src='(.*?)'", html_str_1)[0]
        image_src_2 = re.findall(r"src='(.*?)'", html_str_2)[0]
        date_1 = re.findall(r"</h3>(.*?)<br>", html_str_1)[0]
        date_2 = re.findall(r"<br>(.*?)<br>", html_str_2)[0]
        a_tag_1 = re.findall(r"a href='(..)'", html_str_1)
        a_tag_2 = re.findall(r"a href='(..)'", html_str_2)
        channel_2 = re.findall(r"Channel:.*?s2</a>", html_str_2)[0]
        channel_3 = re.findall(r"Channel:.*?s1</a>", html_str_3)[0]
        self.assertEqual(page_title_1, "RSS news for October 18, 2021 from channel s1")
        self.assertEqual(page_title_2, "RSS news for January 01, 1900 from all channels")
        self.assertEqual(image_src_1, "https://www.rssboard.org/images/rss-man-graphic.png")
        self.assertEqual(image_src_2, "s4")
        self.assertEqual(date_1, "October 18, 2021 - 17:44")
        self.assertEqual(date_2, "18 Oct 2021")
        self.assertEqual(a_tag_1, ["s2", "s6"])
        self.assertEqual(a_tag_2, ["s2"])
        self.assertIn(channel_2, html_str_2)
        self.assertIn(channel_3, html_str_3)

    def test_convert_to_html_web(self):
        """Test to assert that converting to html from web works correctly."""
        test_dict_1 = {"Channel": {"Title": "s0",
                                   "Description": "s1",
                                   "URL": "s2"},
                       "News 1": {"Title": "s3",
                                  "Date": "Mon, 18 Oct 2021 17:44:33 +0300",
                                  "Image": "s5",
                                  "Description": "s6",
                                  "Link": "s7"}}
        test_dict_2 = {"Channel": {"Title": "",
                                   "Description": "s1",
                                   "URL": "s2"},
                       "News 1": {"Title": "s3",
                                  "Date": "18 Oct 2021",
                                  "Image": "s5",
                                  "Description": "s6",
                                  "Link": "s7"}}
        html_str_1 = rss_files.convert_to_html(test_dict_1, None, "s2")
        html_str_2 = rss_files.convert_to_html(test_dict_2, None, "s2")
        heading_1 = re.findall(r"<h1.*?>(.*?)</h1>", html_str_1)[0]
        heading_2 = re.findall(r"<h1.*?>(.*?)</h1>", html_str_2)[0]
        self.assertEqual(heading_1, "RSS news from channel <a href='s2' target='_blank'>s0</a>")
        self.assertEqual(heading_2, "RSS news from channel <a href='s2' target='_blank'>s2</a>")

    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    @patch("sys.stderr", new_callable=StringIO)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=f"{NEW_FOLDER}",
                                           to_pdf=f"{NEW_FOLDER}",
                                           source="https://feeds.skynews.com/feeds/rss/home.xml"))
    def test_write_to_file(self, mock_args, mock_stdout, mock_stderr):
        """Test to assert that HTML and PDF files are created."""
        app.run()
        self.assertTrue(os.path.exists(TEST_HTML))
        self.assertTrue(os.path.exists(TEST_PDF))

    @patch("rss_reader.rss_reader_sql.CACHE_FILE", TEST_DB)
    @patch("logging.error")
    @patch("sys.stderr", new_callable=StringIO)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", return_value="y")
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False, date=None,
                                           clean=False, limit=1, to_html=None,
                                           to_pdf=f"{NEW_FOLDER}",
                                           source="https://lenta.ru/rss/news"))
    def test_pdf_permission_error(self, mock_args, mock_input, mock_stdout, mock_stderr, mock_log):
        """Test to assert that PermissionError in creating PDF file is handled correctly."""
        app.run()
        if os.path.exists(TEST_PDF):
            os.chmod(TEST_PDF, 0o555)
        app.run()
        mock_log.assert_called_once()

    @patch("sys.stderr", new_callable=StringIO)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pdf_no_internet_access(self, mock_stdout, mock_stderr):
        """Test to assert that PDF file is created without internet access."""
        paths = {"to_pdf": f"{NEW_FOLDER}"}
        filenames = rss_files.sanitize_paths(paths)
        html_str = "<html><img src='http://google.com'></html>"

        def guard(*args, **kwargs):
            raise socket.gaierror

        socket.socket.connect = guard
        rss_files.create_files(html_str, filenames)
        self.assertTrue(os.path.exists(TEST_PDF))


if __name__ == "__main__":
    unittest.main()
