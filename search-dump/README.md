search-dump.sh
==============

A simple script for searching through a dump of data, such as compromised
credentials. It has been tested to work with GNU/Linux, BSD, MacOS, and Cygwin
 Bash. For a PowerShell version of this script, see
[Search-Dump.ps1](https://github.com/seanthegeek/powertools/blob/master/Search-Dump.ps1).

Assumptions
-----------

- The data that you want to find is in text format
- The names of the files to be searched end in `.txt` or `.TXT`

Usage
-----

1. Create a list of domains or other terms that you would like to search for,
one term per line. Save the list as `mydomains.csv`
2. Place `mydomains.csv` in the same directory as the files that you wish to
search
3. `cd` to the directory
4. Run `search-dump.sh`

Like any other command, you can redirect the output to a file:

    search-dump.sh > output.csv
