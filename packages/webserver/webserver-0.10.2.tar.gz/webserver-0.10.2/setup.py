#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `__version__.py`.
    """
    with open(os.path.join(package, "__version__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="webserver",
    python_requires=">=3.7",
    version=get_version("webserver"),
    url="https://gitlab.com/harry.sky.vortex/docker-webserver",
    license="Unlicense",
    description="Simple to use CLI for setting up nginx webserver in Docker Swarm and adding websites' configs, proxies and static files",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Igor Nehoroshev",
    author_email="mail@neigor.me",
    packages=["webserver"],
    data_files=[("", ["LICENSE"])],
    include_package_data=True,
    install_requires=["click"],
    extras_require={
        "test": ["asynctest"],
        "lint": ["mypy", "autoflake", "black", "isort"],
    },
    entry_points="""
        [console_scripts]
        webserver=webserver:cli
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
