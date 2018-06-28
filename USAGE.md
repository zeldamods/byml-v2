# Usage

[Releases with a bundled wszst can be found here](https://github.com/leoetlino/byml-v2/releases) for Windows users.

## Dependencies

- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [wszst](https://szs.wiimm.de/download.html#os-cygwin) (in system path, or in a directory that is called 'wszst/' and put next to the converter scripts)

## BYML to YAML

Just run the byml_to_yml script:

```shell
python3 byml_to_yml  PATH_TO_BYML    PATH_TO_YAML
```

**If the byml is compressed, this tool will automatically decompress them.**

To reuse the input file name and only change the extension, use `!!.NEW_EXTENSION` as the second argument.

Example: to convert to YAML in the same directory as the BYML, use `byml_to_yml path_to_botw/Actor/ActorInfo.product.sbyml !!.yml`

## YAML to BYML

```shell
python3 yml_to_byml  PATH_TO_YAML    PATH_TO_BYML
```

**Add `-b` at the end if big endian should be used. For the Wii U version of Breath of the Wild,
you must pass that flag.**

To reuse the input file name and only change the extension, use `!!.NEW_EXTENSION` as the second argument.

If the target file extension starts with `.s`, the tool will **automatically compress**
the BYML using yaz0.

## The YAML format

The generated YAML files are valid, standard YAML.
However you may want to know about the meaning of these special prefixes:

* `!u` before an integer indicates that the value is unsigned. **In general, you should keep
the signedness unchanged.**

* `!l` is for signed 64 bit values. (Not used in BotW.)
* `!ul` is for unsigned 64 bit values. (Not used in BotW.)
* `!f64` is for binary64 floating point values. (Not used in BotW.)

## Advanced usage

By default, if the destination argument is not specified, output will be sent to stdout,
which is handy for looking at bymls without creating temporary files.

If the first argument is not specified either, then these scripts will pipe input from stdin
and output to stdout.
