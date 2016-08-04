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

args = ArgumentParser(description=__doc__)
args.add_argument("URL")
args.add_argument('--version', "-V", action='version', version=__version__)
args.add_argument("--source", "-s", action="store_true", help="save page source")
args.add_argument("--dimensions", "-d", type=str, default="1024x768",
                  help="set the browser window size - 1024x768 by default")
args.add_argument("--user-agent", "-u", nargs="?",
                  help="override the default user-agent string")
args.add_argument("--output", "-o", nargs="?",
                  help="override set the output filename")

args = args.parse_args()

service_args = [
    '--proxy=localhost:8118',
    '--proxy-type=http',
    '--ignore-ssl-errors=true'
    ]

# Use a Google Chrome on Windows 7 User-Agent string by default
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
url = args.URL
if not url.lower().startswith("http://") and not url.lower().startswith("https://"):
    url = "http://{0}".format(url)

dimensions = args.dimensions.lower().split("x")
if len(dimensions) != 2:
    raise ValueError("Dimensions must be a withxheight string")

dimensions = list(map(lambda value: int(value), dimensions))
 
webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = args.user_agent or user_agent

filename = args.output
if filename is None:
    filename = url.split("://")[1]
    filename = filename.split("?")[0]
    filename = filename.split("#")[0]
    filename = filename.strip("/")
    filename = filename.replace("/", "_")

screenshot_filename = "{0}.png".format(filename)

driver = webdriver.PhantomJS(service_args=service_args)
driver.set_window_size(dimensions[0], dimensions[1])
driver.get(url)

driver.save_screenshot(screenshot_filename)
print("Screenshot saved as {0}".format(screenshot_filename))

if args.source:
    source_filename = "{0}.html".format(filename)
    with open(source_filename, "w") as source_file:
        source_file.write(driver.page_source)
    print("Page source saved as {0}".format(source_filename))
