#!/usr/bin/env python
from setuptools import setup

requires = [
    'Werkzeug==0.8.3',
    'Fabric==1.5.1',
]

setup(
    name='Finance Web Application',
    version='1.0',
    description='Website tracking accounts',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/finance',
    install_requires=requires,
)