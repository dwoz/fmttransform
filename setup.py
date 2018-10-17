#!/usr/bin/env python

import sys
from setuptools import setup

setup(
    name='format-tranform',
    version='0.0.1',
    description='Transform Salt serialization formats.',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    author='SaltStack',
    author_email='dwozniak@saltstack.com',
    url='https://github.com/saltstack/transform-format',
    install_requires=[
        'PyYaml',
        'simplejson',
    ],
    scripts=['fmttransform.py'],
#    tests_require=TestCmd.tests_require(),
#    cmdclass = {'test': TestCmd},
)
