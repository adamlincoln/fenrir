#!/bin/python
import os
from setuptools import find_packages
from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



setup(
    # Application name:
    name="fenrir",
    # Version number (initial):
    version="0.1a",

    # Application author details:
    author="Chrys and others",
    author_email="chrys@web.de",

    # Packages
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points = {
        "console_scripts": ['fenrir = fenrir.fenrir:fenrir']
        },

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/chrys87/fenrir/",
    zip_safe=False,
    #
    # license="MIT",
     description="An TTy  Screen Reader For Linux.",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
],
    # Dependent packages (distributions)
    install_requires=[
        "evdev",
        "sox",
    	  	"python-espeak"
    ],
    
)


