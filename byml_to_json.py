#!/usr/bin/env python3
import json
import sys

import byml

if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help']:
    sys.stderr.write("Usage: byml_to_json.py <BYML>")

with open(sys.argv[1], "rb") as file:
    data = file.read()
    root = byml.Byml(data).parse()
    json.dump(root, sys.stdout, indent=2)
