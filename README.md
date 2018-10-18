fmttransform.py
---------------

This program will transform serialization formats from on to another. Currently
json and yaml formats are supported.


Installation
============

Installation can be done using this repositories git url

```
pip install git+git@github.com:dwoz/fmttransform.git#egg=fmttransform
```

This will give you the fmttransform command.

```
$ fmttransform.py --help

usage: fmttransform.py [-h] [--in-dir IN_DIR] [--in-fmt IN_FMT]
                       [--in-filter IN_FILTER] [--out-dir OUT_DIR]
                       [--out-fmt OUT_FMT] [--no-out-ext]

Transform Salt serialization formats.

optional arguments:
  -h, --help            show this help message and exit
  --in-dir IN_DIR       Directory containing input files [default:/Users/dwoz/src/fmttransfer]
  --in-fmt IN_FMT       From format [default:yaml]
  --in-filter IN_FILTER
                        Filter files glob pattern applied to filenames [default:*]
  --out-dir OUT_DIR     Directory to output files too [default:/tmp]
  --out-fmt OUT_FMT     Transform to format [default:json]
  --no-out-ext          Do not change file extension on transform

Example usage:

  fmttransform.py --in-filter='*.yml' --out-dir='/my/out/dir'

  fmttransform.py --in-fmt=json --in-dir='/my/in/dir' --out-fmt=yaml --out-dir='/my/out/dir' --no-out-ext
```



