#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Package definition for PyPI."""
import os

from setuptools import setup

PROJECT_SLUG = "code-snippet"
SOURCE_DIR = "snippet"
__version__ = None

repository_dir = os.path.dirname(__file__)

# Read package version, this will set the variable `__version__` to the current version.
with open(os.path.join(repository_dir, SOURCE_DIR, "_version.py"), encoding="utf8") as fh:
    exec(fh.read())

# Use readme needed as long description in PyPI
with open(os.path.join(repository_dir, "README.md"), encoding="utf8") as fh:
    long_description = fh.read()

setup(
    author="David Hyman, Mbed team",
    author_email="support@mbed.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    description="Code snippet extraction for documentation",
    keywords="documentation-generator documentation-tool snippet-generator snippet project-management documentation",
    include_package_data=True,
    install_requires=["python-dotenv", "toml", "pystache", "mbed-tools-lib"],
    license="Apache 2.0",
    long_description_content_type="text/markdown",
    long_description=long_description,
    name=PROJECT_SLUG,
    packages=[SOURCE_DIR],
    python_requires=">=3.6,<4",
    url=f"https://github.com/ARMmbed/snippet",
    version=__version__,
    entry_points=dict(
        console_scripts=[
            f"snippet = {SOURCE_DIR}.cli:main",
            f"code-snippet = {SOURCE_DIR}.cli:main",
            f"code_snippet = {SOURCE_DIR}.cli:main",
        ]
    ),
)
