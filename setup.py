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
#    packages=['urlio'],
#    install_requires=[
#        'pysmb==1.1.13',
#        'dnspython>=1.12.0',
#        'requests>=2.0.0',
#        'repoze.lru==0.6',
#    ],
#    tests_require=TestCmd.tests_require(),
#    cmdclass = {'test': TestCmd},
)
