from __future__ import unicode_literals
import pytest
import io
import tempfile
import fmttransform
import glob
import mock


def test_read_yaml():
    fp = io.StringIO(
        '\n'.join(
            [
                'foo: |',
                '  bar',
                '  bam',
                '  baz',
            ]
        )
    )
    obj = fmttransform.read_yaml(fp)
    assert obj == {'foo': 'bar\nbam\nbaz'}


def test_read_json():
    fp = io.StringIO('{"foo": "bar\\nbam\\nbaz"}')
    obj = fmttransform.read_json(fp)
    assert obj == {'foo': 'bar\nbam\nbaz'}


def test_write_json():
    obj = {'foo': 'bar\nbam\nbaz'}
    fp = io.StringIO()
    fmttransform.write_json(obj, fp)
    fp.seek(0)
    assert fp.read() == '{"foo": "bar\\nbam\\nbaz"}'


def test_write_yaml():
    obj = {'foo': 'bar\nbam\nbaz'}
    fp = io.StringIO()
    fmttransform.write_yaml(obj, fp)
    fp.seek(0)
    s = fp.read()
    assert s == '"foo": |-\n  bar\n  bam\n  baz\n'


def test_make_dest():
    ret = fmttransform.make_dest('/foo/bar', '/bar/baz', '/foo/bar/bang/bam')
    assert ret == '/bar/baz/bang/bam'


def test_transform():
    fp, path = tempfile.mkstemp()
    with mock.patch('fmttransform.file_transform') as mock_fun:
        fmttransform.transform(path, 'yaml', 'out', 'json')
    assert isinstance(mock_fun.call_args[0][0], io.TextIOWrapper)
    assert isinstance(mock_fun.call_args[0][1], str)
    assert isinstance(mock_fun.call_args[0][2], io.TextIOWrapper)
    assert isinstance(mock_fun.call_args[0][3], str)
