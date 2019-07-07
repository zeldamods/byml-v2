## Simple bymlv2 parser + writer + converters

Features:

* **Supports v2 and v3 files.** These versions are respectively used by
*The Legend of Zelda: Breath of the Wild* and *Super Mario Odyssey*.
* **Supports 64-bit node types** which are used in *Super Mario Odyssey*.
* **Supports both endianness**. The little-endian format is used on the Switch.
* **Cross platform**.
* **Easy to edit and readable output**. No ugly XML. Unobtrusive type information.

### Quick usage

Install Python 3.6+, then run `pip install byml`.

The C module for PyYAML is currently a **hard dependency**. If you are on Windows, you don't have to do anything special. If you are on Linux or on macOS, you will need to install libyaml.

### BYML to YAML

```shell
byml_to_yml  PATH_TO_BYML    PATH_TO_YAML
```

**If the byml is compressed, this tool will automatically decompress them.**

To reuse the input file name and only change the extension, use `!!.NEW_EXTENSION` as the second argument.

Example: to convert to YAML in the same directory as the BYML, use `byml_to_yml path_to_botw/Actor/ActorInfo.product.sbyml !!.yml`

### YAML to BYML

```shell
yml_to_byml  PATH_TO_YAML    PATH_TO_BYML
```

**Add `-b` at the end if big endian should be used. For the Wii U version of Breath of the Wild,
you must pass that flag.**

To reuse the input file name and only change the extension, use `!!.NEW_EXTENSION` as the second argument.

If the target file extension starts with `.s`, the tool will **automatically compress**
the BYML using yaz0.

### Note about YAML integers/floats

* `!u` before an integer indicates that the value is unsigned. **In general, you should keep
the signedness unchanged.**

* `!l` is for signed 64 bit values. (Not used in BotW.)
* `!ul` is for unsigned 64 bit values. (Not used in BotW.)
* `!f64` is for binary64 floating point values. (Not used in BotW.)

### Advanced usage

By default, if the destination argument is not specified, output will be sent to stdout,
which is handy for looking at bymls without creating temporary files.

### Library usage

```python
import byml

parser = byml.Byml(raw_bytes)
document = parser.parse()

writer = byml.Writer(document, be=big_endian_mode, version=byml_version)
writer.write(writable_seekable_stream)
```

### License

This software is licensed under the terms of the GNU General Public License, version 2 or later.
