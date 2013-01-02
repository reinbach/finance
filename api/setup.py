#!/usr/bin/env python
from setuptools import setup

requires = [
    'Flask==0.9',
    'psycopg2==2.4.5',
    'Fabric==1.5.1',
]

setup(
    name='Finance',
    version='1.0',
    description='API tracking accounts',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/finance',
    install_requires=requires,
)