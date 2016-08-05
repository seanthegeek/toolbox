#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Saves a full-page screenshot of a given URL using PhantomJS over
Privioxy->Tor"""

from __future__ import print_function, unicode_literals

from argparse import ArgumentParser

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


__version__ = "1.0.0"

service_args = [
    '--proxy=localhost:8118',
    '--proxy-type=http',
    '--ignore-ssl-errors=true'
    ]

# Spoof a Google Chrome on Windows 7 User-Agent string by default
default_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/51.0.2704.106 Safari/537.36"


def _check_url(url):
    """
    Ensures the URL has a schema by adding http:// to the beginning if it is missing
    Args:
        url: A URL with our without a schema

    Returns:
        A URL with a schema

    """
    if not url.lower().startswith("http://") and not url.lower().startswith("https://"):
        url = "http://{0}".format(url)

    return url


def capture(url, dimensions="1024x768", user_agent=None):
    """
    Captures a screenshot of a web page

    Args:
        url (str): The URL of a page
        dimensions (str): The dimensions of the viewport - 124x768 by default
        user_agent (str): The user-agent string to use - Spoofs Google Chrome on Windows 7 by default

    Returns:
        Screenshot PNG bytes, page source
    """
    dimensions = dimensions.lower().split("x")
    if len(dimensions) != 2:
        raise ValueError("Dimensions must be a widthxheight string")

    dimensions = list(map(lambda value: int(value), dimensions))

    if not user_agent:
        user_agent = default_user_agent

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = user_agent

    url = _check_url(url)
    driver = webdriver.PhantomJS(service_args=service_args)

    dimensions = list(map(lambda value: int(value), dimensions))
    driver.set_window_size(dimensions[0], dimensions[1])
    driver.get(url)
    png_bytes = driver.get_screenshot_as_png()
    page_source = driver.page_source

    return png_bytes, page_source


def _main():
    args = ArgumentParser(description=__doc__)
    args.add_argument("URL")
    args.add_argument('--version', "-V", action='version', version=__version__)
    args.add_argument("--source", "-s", action="store_true", help="save page source")
    args.add_argument("--dimensions", "-d", type=str, default="1024x768",
                      help="set the viewport size - 1024x768 by default")
    args.add_argument("--user-agent", "-u", nargs="?",
                      help="override the user-agent string - Spoofs Google Chrome on Windows 7 by default")
    args.add_argument("--output", "-o", nargs="?",
                      help="override set the output filename")

    args = args.parse_args()

    url = _check_url(args.URL)

    screenshot_bytes, page_source = capture(url, dimensions=args.dimensions, user_agent=args.user_agent)

    filename = args.output
    if filename is None:
        filename = url.split("://")[1]
        filename = filename.split("?")[0]
        filename = filename.split("#")[0]
        filename = filename.strip("/")
        filename = filename.replace("/", "_")

    screenshot_filename = "{0}.png".format(filename)
    with open(screenshot_filename, "wb") as screenshot_file:
        screenshot_file.write(screenshot_bytes)
    print("Screenshot saved as {0}".format(screenshot_filename))

    if args.source:
        source_filename = "{0}.html".format(filename)
        with open(source_filename, "w") as source_file:
            source_file.write(page_source)
        print("Page source saved as {0}".format(source_filename))

if __name__ == "__main__":
    _main()
