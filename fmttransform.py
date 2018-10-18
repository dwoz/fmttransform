#!/usr/bin/env python
'''
Transform Salt serialization formats.

Transform one serialization format to another.
'''
from __future__ import unicode_literals, print_function
import argparse
import fnmatch
import io
import simplejson as json
import logging
import os
import sys
import yaml


logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(
    description='Transform Salt serialization formats.',
    epilog=(
        'Example usage:\n\n'
        '  fmttransform.py --in-filter=\'*.yml\' --out-dir=\'/my/out/dir\'\n\n'
        '  fmttransform.py --in-fmt=json --in-dir=\'/my/in/dir\' '
        '--out-fmt=yaml --out-dir=\'/my/out/dir\' --no-out-ext\n'
    ),
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '--in-dir',
    help='Directory containing input files [default:%(default)s]',
    default=os.path.normpath(os.path.abspath(os.getcwd())),
)
parser.add_argument(
    '--in-fmt',
    help='From format [default:%(default)s]',
    default='yaml',
)
parser.add_argument(
    '--in-filter',
    help=(
        'Filter files glob pattern applied to filenames '
        '[default:%(default)s]'
    ),
    default='*',
)
parser.add_argument(
    '--out-dir',
    help='Directory to output files too [default:%(default)s]',
    default='/tmp',
)
parser.add_argument(
    '--out-fmt',
    help='Transform to format [default:%(default)s]',
    default='json',
)
parser.add_argument(
    '--no-out-ext',
    help='Do not change file extension on transform',
    action='store_true',
    default=False,
)


class TransformException(Exception):
    '''
    Base exception for all transform exceptions to inherit from.
    '''


class BadFormat(TransformException):
    '''
    Raised when an input file is not formatted correctly.
    '''


bad_fmt_exceptions = (
    yaml.parser.ParserError,
    yaml.scanner.ScannerError,
    yaml.reader.ReaderError,
    UnicodeDecodeError,
)


def read_yaml(fp):
    try:
        return yaml.load(fp)
    except bad_fmt_exceptions as exc:
        logger.debug("yaml error: %s", str(exc))
        raise BadFormat


def read_json(fp):
    return json.load(fp)


def write_yaml(obj, fp, encoding='utf-8'):
    yaml.safe_dump(
        obj, fp, encoding=encoding, default_style='|', default_flow_style=False,
    )


def write_json(obj, fp, encoding='utf-8'):
    sobj = json.dumps(obj, indent=2)
    fp.write(sobj.encode(encoding))


readers = {
    'yaml': read_yaml,
    'json': read_json,
}


writers = {
    'yaml': write_yaml,
    'json': write_json,
}


def make_dest(src, dst, filename, ext=''):
    subdir = filename.split(src)[-1]
    out = os.path.join(dst, subdir.lstrip(os.path.sep))
    if ext:
        fname, old_ext = os.path.splitext(out)
        return '{}.{}'.format(fname, ext)
    return out


def transform(source, in_fmt, dest, out_fmt):
    with io.open(source, 'rb') as in_fp:
        with io.open(dest, 'wb') as out_fp:
            file_transform(in_fp, in_fmt, out_fp, out_fmt)


def file_transform(in_fp, in_fmt, out_fp, out_fmt):
    obj = readers[in_fmt](in_fp)
    writers[out_fmt](obj, out_fp)


fmt_to_ext = {
  'yaml': 'yml',
  'json': 'json',
}


def main():
    ns = parser.parse_args()
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(message)s')
    ns.in_dir = os.path.normpath(os.path.abspath(ns.in_dir))
    if ns.no_out_ext:
        ext = None
    else:
        ext = fmt_to_ext[ns.out_fmt]
    for dirname, dirnames, filenames in os.walk(ns.in_dir):
        for filename in filenames:
            if not fnmatch.fnmatch(filename, ns.in_filter):
                logger.debug(
                    'Pattern \'%s\' does not match file %s',
                    ns.in_filter, filename,
                )
                continue
            source = os.path.join(dirname, filename)
            dest = make_dest(ns.in_dir, ns.out_dir, source, ext=ext)
            try:
                os.makedirs(os.path.dirname(dest))
            except OSError as exc:
                if exc.errno != 17:
                    raise
            logger.info(
                "Transform file %s format %s to file %s format %s",
                source, ns.in_fmt, dest, ns.out_fmt,
            )
            try:
                transform(source, ns.in_fmt, dest, ns.out_fmt)
            except BadFormat:
                logger.error(
                    "Bad intput file %s format %s",
                    source, ns.in_fmt
                )


if __name__ == "__main__":
    main()
