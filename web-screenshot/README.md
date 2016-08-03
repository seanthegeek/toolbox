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



Warnings
--------

- Most corporate, university, and other shared networks have policies
prohibiting the use of Tor for security reasons. Tor can help keep what you are
doing hidden, but it will be very obvious to most network administrators when
you use Tor. Get permission if necessary.
- It is possible for a server operator to recognize that a client is using Tor
by checking the IP address against the
[public list of exit nodes](https://check.torproject.org/exit-addresses). Some
sites block these exit nodes, display different content, and/or alert
administrators.

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

Place screenshot.py in the system path, where all users can use it:

$ sudo apt-get install git
$ git clone https://github.com/seanthegeek/toolbox
sudo cp toolbox/web-screenshot/screenshot.py /usr/bin
