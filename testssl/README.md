testssl
=======

```
usage: testssl.py [-h] [--version] [--verbose] input_file output_file

Tests HTTPS certificates

positional arguments:
  input_file   a path to a file containing a list of domains or URLs
  output_file  the path of the output CSV file

optional arguments:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
  --verbose    enable verbose logging
```

Setup
-----

```
sudo apt-get install -y libssl-dev python3-pip
sudo -H pip3 install -U -r requirements.txt
```
