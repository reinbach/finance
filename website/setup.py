#!/usr/bin/env python
from setuptools import setup

requires = [
    'Django==1.4.3',
    'psycopg2==2.4.5',
    'Jinja2==2.6',
    'Coffin==0.3.7',
    'Fabric==1.5.1',
]

setup(
    name='Finance',
    version='1.0',
    description='Website tracking accounts',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/finance',
    install_requires=requires,
)