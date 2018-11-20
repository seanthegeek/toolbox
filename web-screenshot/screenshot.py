#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Saves a full-page screenshot of a given URL using PhantomJS over
Privioxy->Tor"""

from __future__ import print_function, unicode_literals

from argparse import ArgumentParser
import io

from selenium import webdriver

"""Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


__version__ = "2.0.0"

# Spoof a Google Chrome on Windows 7 User-Agent string by default
default_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) " \
                     "AppleWebKit/537.36 " \
                     "(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"


def _standardize_url(url):
    """
    Ensures that the URL has a schema by adding http:// to the beginning if
    it is missing

    Args:
        url (str): A URL with or without a schema

    Returns (str):
        A URL with a schema

    """
    if not url.lower().startswith(
            "http://") and not url.lower().startswith("https://"):
        url = "http://{0}".format(url)

    return url


def url_to_filename(url):
    """
    Generates a filename (without an extension) based on the given URL
    Args:
        url (str): The URL to convert

    Returns (str):
        A filename that closely matches the URL
    """

    url = _standardize_url(url)
    filename = url.split("://")[1]
    filename = filename.split("?")[0]
    filename = filename.split("#")[0]
    filename = filename.strip("/")
    filename = filename.replace("/", "_")

    return filename


def capture(url, dimensions="1024x768", user_agent=None):
    """
    Captures a screenshot of a web page

    Args:
        url (str): The URL of a page
        dimensions (str): The dimensions of the viewport - 124x768 by default
        user_agent (str): The user-agent string to use - Spoofs Google Chrome
        on Windows 7 by default

    Returns:
        Screenshot PNG bytes, page source
    """
    url = _standardize_url(url)
    dimensions = dimensions.lower().split("x")
    if len(dimensions) != 2:
        raise ValueError("Dimensions must be a widthxheight string")

    dimensions = list(map(lambda value: int(value), dimensions))

    if not user_agent:
        user_agent = default_user_agent

    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.customHeaders.User-Agent'] = user_agent
    service_args = [
        '--ignore-ssl-errors=true'
    ]

    # Always use Privoxy
    service_args += ['--proxy=localhost:8118',
                     '--proxy-type=http']

    driver = webdriver.PhantomJS(service_args=service_args)

    dimensions = list(map(lambda value: int(value), dimensions))
    driver.set_window_size(dimensions[0], dimensions[1])
    driver.get(url)
    png_bytes = driver.get_screenshot_as_png()
    page_source = driver.page_source

    return png_bytes, page_source


def _main():
    """
    Run when module is executed as the main module
    Returns:
        None

    """
    args = ArgumentParser(description=__doc__)
    args.add_argument("-V", "--version", action='version', version=__version__)
    args.add_argument("-s", "--source", action="store_true", help="save page source")
    args.add_argument("-t", "--tor", action="store_true", help="use Tor")
    args.add_argument("-d", "--dimensions", type=str, default="1024x768",
                      help="set the viewport size - 1024x768 by default")
    args.add_argument("-u", "--user-agent", nargs="?",
                      help="override the user-agent string - Spoofs Google Chrome on Windows 7 by default")
    args.add_argument("-o", "--output", nargs="?",
                      help="override the output filename")
    args.add_argument("URL")

    args = args.parse_args()
    url = args.URL

    screenshot_bytes, page_source = capture(url, dimensions=args.dimensions, user_agent=args.user_agent, tor=args.tor)

    filename = args.output
    if filename is None:
        filename = url_to_filename(url)

    screenshot_filename = "{0}.png".format(filename)
    with open(screenshot_filename, "wb") as screenshot_file:
        screenshot_file.write(screenshot_bytes)
    print("Screenshot saved as {0}".format(screenshot_filename))

    if args.source:
        source_filename = "{0}.html".format(filename)
        # Use io.open to support utf-8 output in Python 2
        with io.open(source_filename, "w", encoding="utf-8", errors="ignore") as source_file:
            source_file.write(page_source)
        print("Page source saved as {0}".format(source_filename))

if __name__ == "__main__":
    _main()
