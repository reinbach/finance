#!/usr/bin/env python
from setuptools import setup

requires = [
    'Flask==0.10.1',
    'WTForms==1.0.2',
    'SQLAlchemy==0.8.0b2',
    'psycopg2==2.4.5',
    'scales==1.0.3',
    'Fabric==1.5.1',
]

setup(
    name='finance',
    version='0.1',
    description='Finance API for tracking accounts',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/finance',
    install_requires=requires,
)
