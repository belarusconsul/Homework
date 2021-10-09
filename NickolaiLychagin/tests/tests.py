#!/usr/bin/env python3

"""
Tests for pure Python command-line RSS reader.

Usage:

    Windows:

        py -m unittest discover
        (run from package root folder)

    Unix/MacOS:

        python3 -m unittest discover
        (run from package root folder)

    If coverage module installed:

        coverage run -m unittest discover
        coverage report -m
        coverage html

Imported modules:

    argparse
    io
    sys
    xml.etree.ElementTree
    unittest
    patch from unittest.mock import

Classes:

    TestParser(unittest.TestCase) - Tests for argparse functionality.

        Methods:

            test_parse_args
            Test to assert that command-line input is parsed correctly.

            test_limit_positive
            Test to assert that 0 as --limit argument raises parser.error.

    TestErrors(unittest.TestCase) - Tests for catching errors and printing error messages.

        Methods:

            test_urlparse_error
            Test to assert that not valid URL is handled correctly.

            test_url_error
            Test to assert that URLError is caught.

            test_http_error
            Test to assert that HTTPError is caught.

            test_etree_parse_error
            Test to assert that xml.etree.ElementTree.ParseError is caught.

            test_unicode_encode_error
            Test to assert that UnicodeEncodeError is caught.

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

    TestStringMethods(unittest.TestCase) - Tests for correct functionality of string processing.

        Methods:

            test_strip_html
            Test to assert that string is stripped of HTML tags and spaces at the beginning and at the end.

            test_dict_to_text_string
            Test to assert that dictionary is converted to text string correctly.

            test_dict_to_json_string
            Test to assert that dictionary is converted to JSON string correctly.

    TestPrinting(unittest.TestCase) - Tests for printing to console functionality.

        Methods:

            test_print_text_string
            Test to assert that text string is printed to console correctly.

            test_print_json_string
            Test to assert that JSON string is printed to console correctly.
"""

import argparse
import io
import sys
import xml.etree.ElementTree as ET
import unittest
from unittest.mock import patch

from src.rss_reader import rss_reader


class TestParser(unittest.TestCase):
    """
    Tests for argparse functionality.

    Methods:

        test_parse_args
        Test to assert that command-line input is parsed correctly.

        test_limit_positive
        Test to assert that 0 as --limit argument raises parser.error.
    """

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False,
                                           limit=3, source="https://news.yahoo.com/rss/"))
    def test_parse_args(self, mock_args):
        """Test to assert that command-line input is parsed correctly."""
        args = rss_reader.parse_args()
        self.assertEqual(args.json, False)
        self.assertEqual(args.verbose, False)
        self.assertEqual(args.limit, 3)
        self.assertEqual(args.source, "https://news.yahoo.com/rss/")

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False,
                                           limit=0, source="https://news.yahoo.com/rss/"))
    def test_limit_positive(self, mock_stderr, mock_args):
        """Test to assert that 0 as --limit argument raises parser.error."""
        with self.assertRaises(SystemExit):
            rss_reader.parse_args()


class TestErrors(unittest.TestCase):
    """
    Tests for catching errors and printing error messages.

    Methods:

        test_urlparse_error
        Test to assert that not valid URL is handled correctly.

        test_url_error
        Test to assert that URLError is caught.

        test_http_error
        Test to assert that HTTPError is caught.

        test_etree_parse_error
        Test to assert that xml.etree.ElementTree.ParseError is caught.

        test_unicode_encode_error
        Test to assert that UnicodeEncodeError is caught.

        test_rss_channel_error
        Test to assert that situation with no 'channel' tag in XML is handled correctly.

        test_rss_item_error
        Test to assert that situation with no 'item' tag in XML is handled correctly.
    """

    @patch('logging.error')
    def test_urlparse_error(self, mock_log):
        """Test to assert that not valid URL is handled correctly."""
        rss_reader.download_xml("a.com")
        message = "'a.com' does not seem to be a valid URL. Check that valid scheme is provided"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_url_error(self, mock_log):
        """Test to assert that URLError is caught."""
        rss_reader.download_xml("htt://google.com")
        message = "Unable to open 'htt://google.com' due to error - unknown url type: htt"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_http_error(self, mock_log):
        """Test to assert that HTTPError is caught."""
        rss_reader.download_xml("https://google.com/aaa")
        message = "Download of 'https://google.com/aaa' failed with error 404 - Not Found"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_etree_parse_error(self, mock_log):
        """Test to assert that xml.etree.ElementTree.ParseError is caught."""
        rss_reader.download_xml("https://google.com")
        message = "'https://google.com' is not a valid XML"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_unicode_encode_error(self, mock_log):
        """Test to assert that UnicodeEncodeError is caught."""
        rss_reader.download_xml("https://google.ком")
        message = "Source URL must contain only latin characters"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_rss_channel_error(self, mock_log):
        """Test to assert that situation with no 'channel' tag in XML is handled correctly."""
        xml_string = "<rss><channels></channels></rss>"
        root = ET.fromstring(xml_string)
        rss_reader.process_rss(root, 1)
        message = "RSS channel was not found in XML document"
        mock_log.assert_called_with(message)

    @patch('logging.error')
    def test_rss_item_error(self, mock_log):
        """Test to assert that situation with no 'item' tag in XML is handled correctly."""
        xml_string = "<rss><channel></channel></rss>"
        root = ET.fromstring(xml_string)
        rss_reader.process_rss(root, 1)
        message = "No news found in RSS channel"
        mock_log.assert_called_with(message)


class TestVerbose(unittest.TestCase):
    """
    Tests for logging functionality in verbose mode.

    Methods:

        test_log_info
        Test to assert that messages at INFO level are logged to stdout in verbose mode.

        test_log_warning
        Test to assert that messages at WARNING level are logged to stdout in verbose mode.
    """

    @patch('logging.info')
    def test_log_info(self, mock_log):
        """Test to assert that messages at INFO level are logged to stdout in verbose mode."""
        rss_reader.download_xml("https://news.yahoo.com/rss/")
        message = "XML root object created"
        mock_log.assert_called_with(message)

    @patch('logging.warning')
    def test_log_warning(self, mock_log):
        """Test to assert that messages at WARNING level are logged to stdout in verbose mode."""
        root = rss_reader.download_xml("https://www.independent.co.uk/news/uk/rss")
        rss_reader.process_rss(root, 70)
        mock_log.assert_called_once()


class TestDictionary(unittest.TestCase):
    """
    Tests for correct dictionary construction.

    Methods:

        test_dictionary_keys
        Test to assert that dictionary of RSS data has necessary keys.

        test_dictionary_length
        Test to assert that dictionary of RSS data is of correct length.
    """

    def test_dictionary_keys(self):
        """Test to assert that dictionary of RSS data has necessary keys."""
        root = rss_reader.download_xml("https://news.yahoo.com/rss/")
        news_dict = rss_reader.process_rss(root, 3)
        for key in ["Channel", "News 1", "News 2", "News 3"]:
            self.assertIn(key, news_dict.keys())
        for key in ["Title", "Description"]:
            self.assertIn(key, news_dict["Channel"].keys())
        for key in ["Title", "Date", "Image", "Description", "Link"]:
            self.assertIn(key, news_dict["News 1"].keys())

    def test_dictionary_length(self):
        """Test to assert that dictionary of RSS data is of correct length."""
        root = rss_reader.download_xml("https://news.yahoo.com/rss/")
        news_dict = rss_reader.process_rss(root, 4)
        self.assertEqual(len(news_dict), 5)


class TestStringMethods(unittest.TestCase):
    """
    Tests for correct functionality of string processing.

    Methods:

        test_strip_html
        Test to assert that string is stripped of HTML tags and spaces at the beginning and at the end.

        test_dict_to_text_string
        Test to assert that dictionary is converted to text string correctly.

        test_dict_to_json_string
        Test to assert that dictionary is converted to JSON string correctly.
    """

    def test_strip_html(self):
        """Test to assert that string is stripped of HTML tags and spaces at the beginning and at the end."""
        text = "\n<div>Health secretary</div>  \n"
        self.assertEqual(rss_reader.strip_html(text), "Health secretary")

    def test_dict_to_text_string(self):
        """Test to assert that dictionary is converted to text string correctly."""
        test_dict = {'Channel': {'Title': 's1',
                                 'Description': 's2'},
                     'News 1': {'Title': 's3',
                                'Date': 's4',
                                'Image': 's5',
                                'Description': 's6',
                                'Link': 's7'}}
        test_string = rss_reader.dict_to_string(test_dict, False)
        compare_string = '\nFeed: s1\nDescription: s2\n\nTitle: s3\nDate: s4\nImage: s5\ns6\nRead more: s7\n'
        self.assertEqual(test_string, compare_string)

    def test_dict_to_json_string(self):
        """Test to assert that dictionary is converted to JSON string correctly."""
        test_dict = {'Channel': {'Title': 'Новости'}}
        test_string = rss_reader.dict_to_string(test_dict, True)
        compare_string = '{\n    "Channel": {\n        "Title": "Новости"\n    }\n}'
        self.assertEqual(test_string, compare_string)


class TestPrinting(unittest.TestCase):
    """
    Tests for printing to console functionality.

    Methods:

        test_print_text_string
        Test to assert that text string is printed to console correctly.

        test_print_json_string
        Test to assert that JSON string is printed to console correctly.
    """

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=False, verbose=False,
                                           limit=3, source="https://feeds.skynews.com/feeds/rss/home.xml"))
    def test_print_text_string(self, mock_args):
        """Test to assert that text string is printed to console correctly."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        rss_reader.run_rss_reader()
        sys.stdout = sys.__stdout__
        captured_output.seek(1)
        self.assertIn("Sky News", captured_output.readline())
        self.assertIn("Description: ", captured_output.readline())
        captured_output.readline()
        self.assertIn("Title: ", captured_output.readline())
        self.assertIn("Date: ", captured_output.readline())
        self.assertIn("Image: ", captured_output.readline())
        captured_output.readline()
        self.assertIn("Read more: ", captured_output.readline())

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(json=True, verbose=True,
                                           limit=3, source="https://feeds.skynews.com/feeds/rss/home.xml"))
    def test_print_json_string(self, mock_args):
        """Test to assert that JSON string is printed to console correctly."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        rss_reader.run_rss_reader()
        sys.stdout = sys.__stdout__
        captured_output.seek(2)
        self.assertIn('    "Channel": {\n', captured_output.readline())
        self.assertIn('        "Title"', captured_output.readline())
        self.assertIn('        "Description"', captured_output.readline())
        captured_output.readline()
        self.assertIn('    "News 1": {\n', captured_output.readline())
        self.assertIn('        "Title"', captured_output.readline())
        self.assertIn('        "Date"', captured_output.readline())
        self.assertIn('        "Image"', captured_output.readline())
        self.assertIn('        "Description"', captured_output.readline())
        self.assertIn('        "Link"', captured_output.readline())


if __name__ == "__main__":
    unittest.main()
