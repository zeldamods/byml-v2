#!/bin/sh
for filename in byml/*.py; do
  strip-hints $filename | sponge $filename
done
git add -A
git commit -m "Remove type hints for Python 3.5 support"
