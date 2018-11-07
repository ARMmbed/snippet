import os

from setuptools import find_packages
from setuptools import setup

NAME = 'code-snippet'
__version__ = None

repository_dir = os.path.dirname(__file__)

# single source for project version information without side effects
with open(os.path.join(repository_dir, 'src', 'snippet', '_version.py')) as fh:
    exec(fh.read())

with open(os.path.join(repository_dir, 'README.md')) as fh:
    long_description = fh.read()

with open(os.path.join(repository_dir, 'requirements.txt')) as fh:
    requirements = fh.readlines()

setup(
    classifiers=(
        'Intended Audience :: Developers',
    ),
    author="David Hyman, Arm Mbed",
    author_email="support@mbed.com",
    description="Code snippet extraction",
    include_package_data=True,
    install_requires=requirements,
    license='Apache 2.0',
    long_description=long_description,
    name=NAME,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>3.4',
    url="https://github.com/ARMmbed/snippet",
    version=__version__,
)
