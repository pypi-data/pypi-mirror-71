from __future__ import division, print_function

from setuptools import setup, find_packages

VERSION = '0.15.2'

REQUIRED_PACKAGES = [
    'apache-beam>=2.8.0,<3.0.0',
    'SQLAlchemy>=1.2.14,<2.0.0,!=1.3.15',
    'sqlalchemy-utils>=0.33.11,<0.34',
    # Below are drivers for connection to specific DBs
    'pg8000>=1.12.4,<2.0.0',
    'PyMySQL>=0.9.3,<2.0.0',
    'kafka>===1.3.5',
]

REQUIRED_PACKAGES_TEST = [
    'nose>=1.3.7,<2.0.0',
    'testing.postgresql>=1.3.0,<2.0.0',
    'testing.mysqld>=1.4.0,<2.0.0',
    'numpy>=1.15.4,<2.0.0',
    'pandas>=0.23.4,<0.24'
]

REQUIRED_PACKAGES_DOCS = [
    'Sphinx>=1.8.3,<2.0.0',
    'sphinx_rtd_theme>=0.4.2,<2.0.0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sd-beam-nuggets',
    version=VERSION,
    author='Rodrigo Gonçalves',
    author_email='rodrigoalvs.goncalves@gmail.com',
    description='Collection of transforms for the Apache beam python SDK. Forks the original Mohamed Haseeb repository to make some workarounds',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodalgon/beam-nuggets",
    install_requires=REQUIRED_PACKAGES,
    extras_require={'dev': REQUIRED_PACKAGES_TEST + REQUIRED_PACKAGES_DOCS},
    packages=find_packages(exclude=("test", "tests")),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
