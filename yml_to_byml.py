#!/usr/bin/env python3
import argparse
import io
import re
import shutil
import sys
import yaml

import byml

parser = argparse.ArgumentParser(description='Converts a YAML file to BYML.')
parser.add_argument('yml', type=argparse.FileType('rb'), help='Path to a YAML file')
parser.add_argument('-V', '--version', default=2, help='BYML version (1, 2, 3)')
parser.add_argument('-b', '--be', action='store_true', help='Use big endian. Defaults to false.')
args = parser.parse_args()

def strip_literal_suffix(node):
    node.value = node.value.replace('u', '')
    node.value = node.value.replace('l', '')
    return node

loader = yaml.CLoader
yaml.add_constructor(u'tag:yaml.org,2002:int', lambda l, node: byml.Int(l.construct_yaml_int(node)), Loader=loader)
yaml.add_constructor(u'tag:yaml.org,2002:float', lambda l, node: byml.Float(l.construct_yaml_float(node)), Loader=loader)
yaml.add_constructor(u'!u32', lambda l, node: byml.UInt(l.construct_yaml_int(strip_literal_suffix(node))), Loader=loader)
yaml.add_implicit_resolver(u'!u32', re.compile(r'^-?\d+u$', re.X), Loader=loader)
yaml.add_constructor(u'!s64', lambda l, node: byml.Int64(l.construct_yaml_int(strip_literal_suffix(node))), Loader=loader)
yaml.add_implicit_resolver(u'!s64', re.compile(r'^-?\d+l$', re.X), Loader=loader)
yaml.add_constructor(u'!u64', lambda l, node: byml.UInt64(l.construct_yaml_int(strip_literal_suffix(node))), Loader=loader)
yaml.add_implicit_resolver(u'!u64', re.compile(r'^-?\d+ul$', re.X), Loader=loader)
yaml.add_constructor(u'!f64', lambda l, node: byml.Double(l.construct_yaml_float(node)), Loader=loader)

with args.yml as file:
    root = yaml.load(file, Loader=loader)
    buf = io.BytesIO()
    byml.Writer(root, be=args.be, version=args.version).write(buf)
    buf.seek(0)
    shutil.copyfileobj(buf, sys.stdout.buffer)
