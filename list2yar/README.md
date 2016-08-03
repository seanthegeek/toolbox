list2yar.py
===========

    usage: list2yar.py [-h] [--output [OUTPUT]] path

    A simple script that generates a yara rule from a list of strings. It's
    useful for things like generating rules based on lists of domains.

    positional arguments:
      path                  The path the the file containing the strings

    optional arguments:
      -h, --help            show this help message and exit
      --output [OUTPUT], -o [OUTPUT]
                            Override the output path
