import argparse
import io
import os
import shutil
import sys
import yaml

from . import byml
import wszst_yaz0
from . import yaml_util

def main() -> None:
    parser = argparse.ArgumentParser(description='Converts a YAML file to BYML.')
    parser.add_argument('yml', help='Path to a YAML file', nargs='?', default='-')
    parser.add_argument('byml', help='Path to destination BYAML file', nargs='?', default='-')
    parser.add_argument('-V', '--version', default=2, help='BYML version (1, 2, 3)')
    parser.add_argument('-b', '--be', action='store_true', help='Use big endian. Defaults to false.')
    args = parser.parse_args()

    loader = yaml.CSafeLoader
    yaml_util.add_constructors(loader)

    file = sys.stdin if args.yml == '-' else open(args.yml, 'r', encoding='utf-8')
    with file:
        root = yaml.load(file, Loader=loader)
        buf = io.BytesIO()
        byml.Writer(root, be=args.be, version=args.version).write(buf)
        buf.seek(0)

        if args.yml != '-':
            args.byml = args.byml.replace('!!', os.path.splitext(args.yml)[0])
        elif '!!' in args.byml:
            sys.stderr.write('error: cannot use !! (for input filename) when reading from stdin\n')
            sys.exit(1)

        if args.byml != '-':
            extension = os.path.splitext(args.byml)[1]
            if extension.startswith('.s'):
                buf = io.BytesIO(wszst_yaz0.compress(buf.read()))

        output = sys.stdout.buffer if args.byml == '-' else open(args.byml, 'wb')
        with output:
            shutil.copyfileobj(buf, output)

if __name__ == '__main__':
    main()
