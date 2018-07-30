## Simple bymlv2 parser + writer + converters

Features:

* **Supports v2 and v3 files.** These versions are respectively used by
*The Legend of Zelda: Breath of the Wild* and *Super Mario Odyssey*.
* **Supports 64-bit node types** which are used in *Super Mario Odyssey*.
* **Supports both endianness**. The little-endian format is used on the Switch.
* **Cross platform**.
* **Easy to edit and readable output**. No ugly XML. Unobtrusive type information.

### Quick usage

```shell
byml_to_yml   PATH_TO_BYML
yml_to_byml   PATH_TO_YAML
```

Output will be sent to stdout and can be piped into a file. Pass `-` as the path to read from stdin.

### Library

```python
import byml

parser = byml.Byml(raw_bytes)
document = parser.parse()

writer = byml.Writer(document, be=big_endian_mode, version=byml_version)
writer.write(writable_seekable_stream)
```

### Note about YAML integers/floats

The initial version of this library supported automatic type detection.

However, the problem with automatic type detection is that Nintendo sometimes
uses signed integers even when it makes no sense and their byml
library will only look for int nodes. Other times they will use
uints for the same data type (crc32 hashes).

It's totally unpredictable.

So we need to keep type information when dumping/loading files
instead of guessing types.

To keep YAML output easy to read and write, the converter scripts will use
prefixes to indicate types for literals:

* Unsigned integers will get a 'u' prefix.
* 64 bit types will additionally get a 'l'.

### License

This software is licensed under the terms of the GNU General Public License, version 2 or later.
