#!/user/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

try:
    with open('README.md', errors='replace') as f:
        readme = f.read()
except IOError:
    readme = ''


# requirements
here = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(here, 'requirements.txt')) as fp:
        install_requires = fp.read()
except Exception:
    install_requires = ""

setup(
    name="srudp",
    version="0.3.3",
    url='https://github.com/namuyan/srudp',
    author='namuyan',
    description='secure reliable udp socket implemented by PurePython',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires,
    license="MIT Licence",
    keywords='RUDP UDP P2P hole-punching',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)
