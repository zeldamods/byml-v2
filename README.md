## Simple bymlv2 parser + writer + converters

Features:

* **Supports v2 and v3 files.** These versions are respectively used by
*The Legend of Zelda: Breath of the Wild* and *Super Mario Odyssey*.
* **Supports 64-bit node types** which are used in *Super Mario Odyssey*.
* **Supports both endianness**. The little-endian format is used on the Switch.
* **Cross platform**. And not as an afterthought.
* **Easy to edit and readable output**. No ugly XML and type information. Types will be automagically chosen just like Nintendo's own converter.

### Usage

```shell
byml_to_json.py  PATH_TO_BYML
byml_to_yml.py   PATH_TO_BYML
yml_to_byml.py   PATH_TO_YAML
```

Output will be sent to stdout and can be piped into a file.

### Library

```python
import byml

parser = byml.Byml(raw_bytes)
document = byml.Byml(raw_bytes).parse()

writer = byml.Writer(document, be=big_endian_mode, version=byml_version)
writer.write(writable_seekable_stream)
```
