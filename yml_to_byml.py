#!/usr/bin/env python3
import argparse
import io
import shutil
import sys
import yaml

import byml

parser = argparse.ArgumentParser(description='Converts a YAML file to BYML.')
parser.add_argument('yml', type=argparse.FileType('rb'), help='Path to a YAML file')
parser.add_argument('-V', '--version', default=2, help='BYML version (1, 2, 3)')
parser.add_argument('-b', '--be', action='store_true', help='Use big endian. Defaults to false.')
args = parser.parse_args()

with args.yml as file:
    root = yaml.load(file)
    buf = io.BytesIO()
    byml.Writer(root, be=args.be, version=args.version).write(buf)
    buf.seek(0)
    shutil.copyfileobj(buf, sys.stdout.buffer)
