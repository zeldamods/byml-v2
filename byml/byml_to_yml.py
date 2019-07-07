import argparse
import json
import os
import sys
import yaml

from . import byml
import wszst_yaz0
from . import yaml_util

def main() -> None:
    parser = argparse.ArgumentParser(description='Converts a BYML file to YAML.')
    parser.add_argument('-j', '--to-json', action='store_true', help='Convert to JSON (warning: one-way conversion; does not preserve type information)')
    parser.add_argument('byml', help='Path to a BYML file', nargs='?', default='-')
    parser.add_argument('yml', help='Path to destination YAML file', nargs='?', default='-')
    args = parser.parse_args()

    dumper = yaml.CDumper
    yaml_util.add_representers(dumper)

    file = sys.stdin.buffer if args.byml == '-' else open(args.byml, 'rb')
    with file:
        data = file.read()
        if data[0:4] == b'Yaz0':
            data = wszst_yaz0.decompress(data)
        root = byml.Byml(data).parse()

        if args.byml != '-':
            args.yml = args.yml.replace('!!', os.path.splitext(args.byml)[0])
        elif '!!' in args.yml:
            sys.stderr.write('error: cannot use !! (for input filename) when reading from stdin\n')
            sys.exit(1)
        output = sys.stdout if args.yml == '-' else open(args.yml, 'w', encoding='utf-8')
        with output:
            if args.to_json:
                json.dump(root, output, ensure_ascii=False)
            else:
                yaml.dump(root, output, Dumper=dumper, allow_unicode=True, encoding='utf-8', default_flow_style=None)

if __name__ == '__main__':
    main()
