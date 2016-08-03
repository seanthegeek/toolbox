#!/usr/bin/env python

"""A simple script that generates a yara rule from a list of strings. It's
useful for things like generating rules based on lists of domains."""

from __future__ import print_function, unicode_literals

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

from argparse import ArgumentParser
from os.path import basename
from collections import OrderedDict
from datetime import datetime

__version__ = "1.0.0"

args = ArgumentParser(description=__doc__)
args.add_argument("path", help="The path the the file containing the strings")
args.add_argument("--output", "-o", nargs="?", help="Override the output path")

args = args.parse_args()

meta = OrderedDict(generated_by="list2yar v{0}".format(__version__),
                   generated_on=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

rule_name = basename(args.path).split(".")[0]

with open(args.path) as input_file:
    strings = list(map(lambda line: line.strip(), input_file.readlines()))

meta_string = ""

for key in meta.keys():
    meta_string += '        {0} = "{1}"\n'.format(key, meta[key])

strings_string = ""

for i in range(len(strings)):
    line = i + 1
    strings_string += '        ${0} = "{1}" fullword ascii wide nocase\n'.format(line, strings[i])


rule_string = """rule {0}
{{
    meta:
{1}
    strings:
{2}
    condition:
        any of them
}}
""".format(rule_name, meta_string, strings_string)

output_path = args.output or "{0}.yar".format(rule_name)

with open(output_path, "w") as output_file:
    output_file.write(rule_string)

print("Generated {0}".format(output_path))
