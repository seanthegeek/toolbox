#!/bin/bash

tmpfile=$(mktemp /tmp/dumpsearch.XXXXXX)

cat mydomains.csv | tr -d "\r" > $tmpfile

fgrep -iR -f $tmpfile --include "*.txt" --include "*.TXT" | sort | uniq

rm "$tmpfile"
