#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, Command

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('gnotify/gnotify.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.egg-info')


setup(
    name="gnotify",
    entry_points={
        "console_scripts": ['gnotify = gnotify.gnotify:main']
    },
    cmdclass={
        "clean": CleanCommand,
    },
    version=version,
    description="Get notified on your Google Home device from text-to-speech",
    long_description=long_descr,
    author="Benoît Bourgeois",
    author_email="bierdok@gmail.com",
    packages=["gnotify"],
    install_requires=[
        "cachier == 1.2.4",
        "pychromecast == 2.3.0",
        "pymongo == 3.7.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
