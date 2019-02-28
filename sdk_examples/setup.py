#!/usr/env/bin python
# -*- coding: utf-8 -*-

import os
import re
import codecs

from setuptools import setup

'''
sdk examples启动文件
'''

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='sdk_lib',
    version='0.1',
    license='GPL',
    author_email='xx@xx.com',
    description='aliyun sdk_examples library.',
    packages=['sdk_lib'
              ],
    zip_safe=False,
    py_modules=[],
    package_data = {'': ['*.conf']}
)
