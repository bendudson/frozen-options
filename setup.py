from setuptools import setup

import frozen_options

setup(
    name     = 'frozen_options',
    version  = frozen_options.__version__,
    url      = 'https://github.com/bendudson/frozen-options',

    author       = 'Ben Dudson',
    author_email = 'benjamin.dudson@york.ac.uk',

    packages = ['frozen_options'],
    license  = 'MIT License',

    description      = 'An immutable dictionary for configuration options',
    long_description = open('README.org').read()
)
