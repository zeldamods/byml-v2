#!/usr/bin/env python3
import argparse
import os
import re
import sys
import yaml

import byml
import yaz0_util

parser = argparse.ArgumentParser(description='Converts a BYML file to YAML.')
parser.add_argument('byml', help='Path to a BYML file', nargs='?', default='-')
parser.add_argument('yml', help='Path to destination YAML file', nargs='?', default='-')
args = parser.parse_args()

dumper = yaml.CDumper
yaml.add_representer(byml.Int, lambda d, data: d.represent_int(data), Dumper=dumper)
yaml.add_representer(byml.Float, lambda d, data: d.represent_float(data), Dumper=dumper)
yaml.add_representer(byml.UInt, lambda d, data: d.represent_scalar(u'!u', '0x%08x' % data), Dumper=dumper)
yaml.add_representer(byml.Int64, lambda d, data: d.represent_scalar(u'!l', str(data)), Dumper=dumper)
yaml.add_representer(byml.UInt64, lambda d, data: d.represent_scalar(u'!ul', str(data)), Dumper=dumper)
yaml.add_representer(byml.Double, lambda d, data: d.represent_scalar(u'!f64', str(data)), Dumper=dumper)

file = sys.stdin.buffer if args.byml == '-' else open(args.byml, 'rb')
with file:
    data = file.read()
    if data[0:4] == b'Yaz0':
        data = yaz0_util.decompress(data)
    root = byml.Byml(data).parse()

    if args.byml != '-':
        args.yml = args.yml.replace('!!', os.path.splitext(args.byml)[0])
    elif '!!' in args.yml:
        sys.stderr.write('error: cannot use !! (for input filename) when reading from stdin\n')
        sys.exit(1)
    sys.stderr.write('writing to %s\n' % args.yml)
    output = sys.stdout if args.yml == '-' else open(args.yml, 'w')
    with output:
        yaml.dump(root, output, Dumper=dumper, allow_unicode=True)
