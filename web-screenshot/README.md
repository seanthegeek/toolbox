screenshot.py
=============

    Saves a full-page screenshot of a given URL using PhantomJS over Privioxy->Tor
    
    positional arguments:
      URL
    
    optional arguments:
      -h, --help            show this help message and exit
      --version, -V         show program's version number and exit
      --source, -s          save page source
      --dimensions DIMENSIONS, -d DIMENSIONS
                            set the viewport size - 1024x768 by default
      --user-agent [USER_AGENT], -u [USER_AGENT]
                            override the user-agent string - Spoofs Google Chrome
                            on Windows 7 by default
      --output [OUTPUT], -o [OUTPUT]
                            override the output filename



Factions
--------

### capture(url, dimensions="1024x768", user_agent=None)
    
        Captures a screenshot of a web page
        
        Args:
            url (str): The URL of a page
            dimensions (str): The dimensions of the viewport - 124x768 by default
            user_agent (str): The user-agent string to use - Spoofs Google Chrome on Windows 7 by default
    
        Returns:
            Screenshot PNG bytes, page source
 
 
### standardize_url(url)

    Ensures that the URL has a schema by adding http:// to the beginning if it is missing

    Args:
        url (str): A URL with or without a schema

    Returns (str):
        A URL with a schema


### url_to_filename(url)

    Generates a filename (without an extension) based on the given URL

    Args:
        url (str): The URL to convert

    Returns (str):
        A filename that closely matches the URL

 
Example screenshots
-------------------
 
 - [check.torproject.org](https://imgur.com/z3sRZjU)
 - [useragentstring.com](https://imgur.com/8SJ4uwL)
 - [cnn.com](https://imgur.com/pYrkAdj)

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

Rather not use Tor? Skip the Tor part of the setup. 

Setup
-----

Install Tor.

For Debian systems, **excluding** Ubuntu, you can just run:

    $ sudo apt-get install tor

For all other Debian-based Linux distros, follow option two of this guide from the
Tor Project

https://www.torproject.org/docs/debian.html.en

Or for CentOS/RHEL/Fedora:

https://www.torproject.org/docs/rpms.html.en

Install Privioxy

    $ sudo apt-get install privoxy

Configure Privioxy

    $ sudo nano /etc/privoxy/config

If you want to use Tor, locate and uncomment the following line:

    #        forward-socks5t             /     127.0.0.1:9050 .

__Or__, to forward to an HTTP proxy, add a line like this one:

      forward   /      parent-proxy.example.org:8080
      
More proxy forwarding configuration examples can be found
[here](https://www.privoxy.org/user-manual/config.html#FORWARD).

If you just want Privoxy to access the web directly, no configuration
canges are needed.

Restart Privoxy:

    $ sudo service privoxy restart

Install PhantomJS (the project's [static build](http://phantomjs.org/download.html), **not** from a repository)

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

### Why is Privoxy used?

While PhantomJS is capable of using internet connections, HTTP proxies,
and Tor's SOCKS5 proxy directly, PhantomJS does not return HTTP status
codes or error details. Privoxy will return error details to the browser
as an HTML page, which will be captured in the screenshot.
