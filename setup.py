#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import os


# Package meta-data.
NAME = 'titanic-classification-model'
DESCRIPTION = "A Package of Titanic classification model with the original dataset."
URL = "https://github.com/singultek/deploy_ml_titanic"
EMAIL = "singultek@gmail.com"
AUTHOR = "Sinan Gültekin"
REQUIRES_PYTHON = "==3.11.1"

long_description = DESCRIPTION

# Load the package's VERSION file as a dictionary.
about = {}
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_DIR = os.path.join(ROOT_DIR, "requirements")
PACKAGE_DIR = os.path.join(ROOT_DIR, "classification_model")
with open(os.path.join(PACKAGE_DIR, "VERSION")) as f:
    _version = f.read().strip()
    about["__version__"] = _version


# What packages are required for this module to be executed?
def list_reqs(fname="requirements.txt"):
    with open(os.path.join(REQUIREMENTS_DIR, fname)) as fd:
        return fd.read().splitlines()

# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"classification_model": ["VERSION"]},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license_files=('LICENSE.txt',),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)