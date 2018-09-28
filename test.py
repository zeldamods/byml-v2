#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys

def byml_to_yml(data: bytes) -> bytes:
    return subprocess.run(['byml_to_yml'], input=data,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout

def yml_to_byml(data: bytes) -> bytes:
    return subprocess.run(['yml_to_byml'], input=data,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout

def die(m: str) -> None:
    sys.stderr.write(m + '\n')
    sys.exit(1)

for path in Path(os.path.dirname(os.path.realpath(__file__))).glob('test_data/*.byml'):
    print(path.name)

    byml_data = path.open('rb').read()
    loaded_yml_data = byml_to_yml(byml_data)
    yml_data = path.with_suffix('.yml').open('rb').read()
    if loaded_yml_data != yml_data:
        die('  parse FAIL: generated YAML does not match known output')
    print('  parse OK')

    roundtrip_yml_data = byml_to_yml(yml_to_byml(yml_data))
    if roundtrip_yml_data != yml_data:
        die('  roundtrip test FAIL: byml_to_yml(yml_to_byml(x)) != x')
    print('  roundtrip OK')
