#!/usr/bin/env python3
"""
Packaging setup for gitcln.
"""
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

# local import
import gitcln as package


def rfile(fname):
    """Get README.md file content.

    :param fname: RAEDME file name
    :type fname: str
    """
    with open(join(abspath(dirname(__file__)), fname), "r", encoding="utf-8") as readme:
        return readme.read()


# gitcln setup
setup(
    python_requires=">=3",
    name=package.__name__,
    version=package.__version__,
    license=package.__license__,
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    long_description=rfile("README.md"),
    long_description_content_type="text/markdown",
    url=package.__url__,
    packages=find_packages(exclude=["test*"]),
    include_package_data=True,
    keywords=["python", "cli", "tools", "cleaner", "git-tools"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["gitcln = gitcln.gitcln:main",],},
)
