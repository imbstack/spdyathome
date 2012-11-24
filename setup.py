#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.9'

setup(
  name = 'spdyathome',
  version = version,
  description = 'Testing SPDY vs HTTP',
  author = 'Brian Stack',
  author_email = 'bis12@case.edu',
  url = 'http://github.com/bis12/spdyathome',
  download_url = \
    'http://github.com/bis12/spdyathome/tarball/spdyathome-%s' % version,
  packages = find_packages('spdyathome'),
  provides = ['spdyathome'],
  scripts = ['scripts/spdyathome'],
  long_description = open("README.md").read(),
  install_requires = [
    'pyyaml >= 3.09',
    'thor',
    'argparse==1.2.1',
    'progress==1.0.2'
  ],
  dependency_links = ['git://github.com/bis12/thor.git@spdy#egg=thor'],
  classifiers = [
    'Development Status :: 3 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
  ]
)
