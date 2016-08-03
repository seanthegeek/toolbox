#!/usr/bin/python

"""Saves a screenshot of a given URL using PhantomJS over Privioxy/Tor"""

from __future__ import print_function, unicode_literals

from argparse import ArgumentParser

from selenium import webdriver

__version__ = "1.0.0"

args = ArgumentParser(description=__doc__)
args.add_argument("URL")
args.add_argument("--dimensions", "-d", type=str, default="1024x768",
                  help="Sets the browser window size - 1024x768 by default")
args.add_argument("--user-agent", "-u", nargs="?",
                  help="Overrides the default user-agent string")
args.add_argument("--output", "-o", nargs="?",
                  help="Optionally set the output filename")

args = args.parse_args()

service_args = [
    '--proxy=localhost:8118',
    '--proxy-type=http',
    '--ignore-ssl-errors=true'
    ]

url = args.URL
if not url.lower().startswith("http://") and not url.lower().startswith("https://"):
    url = "http://{0}".format(url)

dimensions = args.dimensions.lower().split("x")
if len(dimensions) != 2:
    raise ValueError("Dimensions must be a withxheight string")

dimensions = map(lambda value: int(value), dimensions)

user_agent = args.user_agent
if user_agent:
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = user_agent

filename = args.output
if filename is None:
    filename = url.split("://")[1]
    filename = filename.split("?")[0]
    filename = filename.split("#")[0]
    filename = filename.strip("/")
    filename = filename.replace("/", "_")

filename = "{0}.png".format(filename)

driver = webdriver.PhantomJS(service_args=service_args)
driver.set_window_size(dimensions[0], dimensions[1])
driver.get(url)
driver.save_screenshot(filename)

print("Screenshot saved as {0}".format(filename))
