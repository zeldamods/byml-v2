## Simple bymlv2 parser + converter

Features:

* **Handles v2 files properly.** This is the version that is used by
*The Legend of Zelda: Breath of the Wild*.
* **Supports 64-bit node types** which are used in *Super Mario Odyssey*.
* **Cross platform**. And not as an afterthought.
* **Handles both endianness correctly**. The little-endian format is used on the Switch.

### Usage

```
byml_to_json.py  PATH_TO_BYML
byml_to_yml.py   PATH_TO_BYML
```

Output will be sent to stdout and can be piped into a file.

#### Library

```
import byml

parser = byml.Byml(raw_bytes)
document = byml.Byml(raw_bytes).parse()

writer = byml.Writer(document, be=big_endian_mode, version=byml_version)
writer.write(writable_seekable_stream)
```
