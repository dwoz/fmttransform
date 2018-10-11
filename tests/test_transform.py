from __future__ import unicode_literals
import pytest
import io
import fmttransform
import glob


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


def test_write_json():
    obj = {'foo': 'bar\nbam\nbaz'}
    fp = io.StringIO()
    fmttransform.write_json(obj, fp)
    fp.seek(0)
    assert fp.read() == '{"foo": "bar\\nbam\\nbaz"}'
