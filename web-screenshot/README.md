screenshot.py
=============

    usage: screenshot.py [-h] [--dimensions DIMENSIONS]
                         [--user-agent [USER_AGENT]] [--output [OUTPUT]]
                         URL

    Saves full-page a screenshot of a given URL using PhantomJS over
    Privioxy->Tor

    positional arguments:
      URL

    optional arguments:
      -h, --help            show this help message and exit
      --dimensions DIMENSIONS, -d DIMENSIONS
                            Sets the browser window size - 1024x768 by default
      --user-agent [USER_AGENT], -u [USER_AGENT]
                            Overrides the default user-agent string
      --output [OUTPUT], -o [OUTPUT]
                            Optionally set the output filename



Tor warnings
------------

- Most corporate, university, and other shared networks have policies
prohibiting the use of Tor for security reasons. Tor can help keep what you are
doing hidden, but it will be very obvious to most network administrators when
you use Tor. Get permission if necessary.
- It is possible for a server operator to recognize that a client is using Tor
by checking the IP address against the
[public list of exit nodes](https://check.torproject.org/exit-addresses). Some
sites block these exit nodes, display different content, and/or alert
server operators.

Rather not use Tor? Skip the Tor and Privoxy parts of the setup, and remove the
or modify the proxy options as needed in the `service_options` list, which is
located near the top of `screenshot.py`. In that case, it is strongly advised
to use a separate, unattributable connection.

Setup
-----

Install Tor.

For Debian systems, **excluding** Ubuntu, you can just run:

    $ sudo apt-get install tor

For all other Linux distros, follow option two of this guide from the
Tor Project

https://www.torproject.org/docs/debian.html.en

Or for CentOS:

https://www.torproject.org/docs/rpms.html.en

Install Privioxy

    $ sudo apt-get install privoxy

Configure Privioxy

$ sudo nano /etc/privoxy/config

Locate, and uncomment the following line:

    #        forward-socks5t             /     127.0.0.1:9050 .

Restart Privoxy:

    $ sudo service privoxy restart

Install PhantomJS (the project's static build, **not** from a repository)

    $ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-x.x.x-linux-x86_64.tar.bz2
    $ bunzip2 phantomjs-x.x.x-linux-x86_64.tar.bz2
    $ sudo cp phantomjs-x.x.x-linux-x86_64/bin/phantomjs /usr/bin

Install Selenium for Python

    $ sudo apt-get install python-pip
    $ sudo pip install selenium

Place `screenshot.py` in the system path, where all users can use it:

    $ sudo apt-get install git
    $ git clone https://github.com/seanthegeek/toolbox
    $ sudo cp toolbox/web-screenshot/screenshot.py /usr/bin

FAQ
---

### Why is the background of the page black?

If no background is specified by the web page, most browsers will render a
white background. However, PhantomJS (the headless browser used by
`screenshot.py`) will save a transparent background in that case, which  will
appear black in many photo viewers, including the Windows photo viewer.

The quickest way to fix this is to open the screenshot in Microsoft Paint, and
save over it. You will receive a warning about loosing transparency, which is
exactly what you want. Other image editors like GIMP and Adobe Photoshop
also have options to disable transparency when saving PNGs.

## Why is Privoxy used in between PhantomJS and Tor?

While PhantomJS is capable of using Tor's SOCKS5 proxy directly, PhantomJS does
not return HTTP status codes or error details. Privoxy will return error
details to the browser as an HTML page, which will be captured in the
screenshot.
