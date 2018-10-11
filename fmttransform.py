'''
Transform Salt serialization formats.

Transform one serialization format to another.
'''
from __future__ import unicode_literals, print_function
import io
import os
import sys
import logging
import yaml
import fnmatch
import json

import argparse

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description='Transform Salt serialization formats.',
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
    help='Directory to output files too',
    default='/tmp',
)
parser.add_argument(
    '--out-fmt',
    help='Transform to format',
    default='json',
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
        logger.error("yaml error: %s", str(exc))
        raise BadFormat


def read_json(fp):
    return json.load(fp)


def write_yaml(obj, fp):
    return yaml.dump(obj, fp)


def write_json(obj, fp):
    return json.dump(obj, fp)


readers = {
    'yaml': read_yaml,
    'json': read_json,
}


writers = {
    'yaml': write_yaml,
    'json': write_json,
}


def make_dest(src, dst, filename):
    subdir = os.path.basename(filename.split(src)[-1])
    return os.path.join(dst, subdir)


def transform(source, in_fmt, dest, out_fmt):
    with io.open(source, 'r', encoding='utf-8') as in_fp:
        with io.open(dest, 'w', encoding='utf-8') as out_fp:
            file_transform(in_fp, in_fmt, out_fp, out_fmt)


def file_transform(in_fp, in_fmt, out_fp, out_fmt):
    obj = readers[in_fmt](in_fp)
    writers[out_fmt](obj, out_fp)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    ns = parser.parse_args()
    ns.in_dir = os.path.normpath(os.path.abspath(ns.in_dir))
    for dirname, dirnames, filenames in os.walk(ns.in_dir):
        for filename in filenames:
            if not fnmatch.fnmatch(filename, ns.in_filter):
                logger.debug(
                    'Pattern \'%s\' does not match file %s',
                    ns.in_filter, filename,
                )
                continue
            source = os.path.join(dirname, filename)
            dest = make_dest(ns.in_dir, ns.out_dir, source)
            try:
                os.makedirs(os.path.dirname(dest))
            except OSError as exc:
                if exc.errno != 17:
                    raise
            logger.info(
                "Transform file %s format %s to file %s format %s",
                source, in_fmt, dest, out_fmt,
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
