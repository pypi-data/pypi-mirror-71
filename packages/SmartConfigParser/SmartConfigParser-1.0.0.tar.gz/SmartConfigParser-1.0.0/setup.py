#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname


def read(fname):
    return open(join(dirname(__file__), fname)).read()


PKG = 'SmartConfigParser'
VERSION = '1.0.0'

setup(
    name=PKG,
    version=VERSION,
    description="Simplifies and enchances functionalities in Python's ConfigParser",
    long_description=read('README.rst'),
    author="Cédric RICARD",
    author_email="ricard33@gmail.com",
    url="http://github.com/ricard33/smartconfigparser",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms=['any'],
    install_requires=[],
    license="MIT License",
    keywords="ConfiParser,ini",
    zip_safe=True,
    test_suite="tests",
    tests_require=['setuptools'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
