#!/usr/bin/env python

import functools
import os
from setuptools import find_packages
import sys

from setuptools import setup

import resta

root = os.path.dirname(__file__)
root = os.path.abspath(root)
root = os.path.normpath(root)

path = functools.partial(os.path.join, root)

run_deps = open(path('requirements.txt')).readlines()
test_deps = ['pytest']
setup_deps = []

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_deps.append('pytest-runner')

setup(
    name='RESTa',
    version=resta.__version__,
    author='Dmitry Bogun',
    author_email='nyaka@nyaka.org',
    description='REST API client framework',
    long_description=open(path('README.md')).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/surabujin/resta',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(),
    setup_requires=setup_deps,
    tests_require=test_deps,
    install_requires=run_deps,
)
