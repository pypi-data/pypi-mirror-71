# Yet Another Argument Parser (Yaap) #

This is a sugar-coated wrapper for python's standard library `argparse` that 
improves the library by the following ways.

  * Yaap standardizes argument types into `int`, `float`, `bool`, `str`, `path`,
    and the respective `list` types. If you are interested in having custom
    types, you may skip this library.
  
  * Yaap allows arguments to be specified using `json` or `yaml` configuration
    files. There are several other libraries that I am aware of that achieves
    similar effects. `argparse` itself allows arguments to be listed using 
    line-delimited text file using `fromfile_prefix_char` option, but the
    readability is poor. [`ConfigArgParse`](https://pypi.org/project/ConfigArgParse/)
    also provides similar functionality, but it uses in-house yaml/json parser
    that works poorly in some cases. Yaap uses standard `pyyaml` to parse
    configuration files.
  
  * Yaap offers configuration validation using `jsonschema`, ensuring integrity
    of the input configuration file. 


## Installation ##

Yaap can be installed from pypi.

    $ pip install yaap


## Quickstart ##

Create parsers by filling in intended argument type object into `parser.add`.

```python

from yaap import *

parser = Yaap()
parser.add(Int(
    "int", shortcut="i", min_bound=0, required=True
))
parser.add(IntList(
    "int-list"
))
parser.add(Float(
    "float", min_bound=-2.0, required=True
))
parser.add(FloatList(
    "float-list", min_bound=2.0, multiples=5.0
))
parser.add(Path(
    "path", must_exist=True, required=True
))
parser.add(Path(
    "dir", must_exist=True, is_dir=True
))
parser.add(Str(
    "str", regex=r"[a-c][0-9]"
))
parser.add(StrList(
    "str-list", min_length=3
))
parser.add(Bool(
    "bool", help="this is a bool"
))
```

Call `parser.parse` to perform argument parsing.

```python
args = parser.parse(
    "--int 3 --int-list 2 3 --float 3.0 --float-list 5 10 "
    "--path tests/test.json --dir tests --str b5 "
    "--str-list abc defg --bool".split()
)
```

The resulting object is a dictionary.

```
>>> import pprint; pprint.pprint(args)
{'bool': True,
 'dir': '/Users/kani/Clouds/Dropbox/Codes/Python/yaap/tests',
 'float': 3.0,
 'float_list': [5.0, 10.0],
 'int': 3,
 'int_list': [2, 3],
 'path': '/Users/kani/Clouds/Dropbox/Codes/Python/yaap/tests/test.json',
 'str': 'b5',
 'str_list': ['abc', 'defg']}
```

Resulting arguments can be validated against the `parser`.

```python
# This will throw `ValidationError` if the validation fails.
parser.validate(args)
```

## License ##

MIT License
