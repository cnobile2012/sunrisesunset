# -*- coding: utf-8 -*-
"""
Setup a pip environment.
"""
__docformat__ = "restructuredtext en"

import os
import re
from setuptools import setup

filepath = os.path.dirname(__file__)

def version():
    """
    Find the version.

    :return: The version.
    :rtype: str
    """
    regex = r'(?m)(^{}[\s]*=[\s]*(?P<ver>\d*)$)'
    fullpath = os.path.join(filepath, 'include.mk')

    with open(fullpath, mode='r', encoding='UTF-8') as f:
        ver = f.read()

    major = re.search(regex.format('MAJORVERSION'), ver).group('ver')
    minor = re.search(regex.format('MINORVERSION'), ver).group('ver')
    patch = re.search(regex.format('PATCHLEVEL'), ver).group('ver')
    # Look for a tag indicating a pre-release candidate. ex. rc1
    env_value = os.environ.get('PR_TAG', '')
    return f"{major}.{minor}.{patch}{env_value}"

filename = os.path.join(filepath, 'README.rst')

with open(filename, mode='r', encoding='UTF-8') as readme:
    README = readme.read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sunrisesunset',
    version=version(),
    packages=['sunrisesunset',],
    include_package_data=True,
    license='MIT',
    description=("This class provides the sunrise and sunset times for "
                 "various zeniths, latitudes and longitudes."),
    long_description=README,
    url='https://github.com/cnobile2012/sunrisesunset',
    author='Carl J. Nobile',
    author_email='carl.nobile@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Astronomy'
        ]
    )
