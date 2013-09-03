#!/usr/bin/env python
import os

from pip.req import parse_requirements
from setuptools import setup

install_reqs = parse_requirements(os.path.join(os.path.abspath(__file__), 'requirements.txt'))
reqs = [str(r.req) for r in install_reqs]

setup(
    name='finance',
    version='0.1',
    description='Finance API for tracking accounts',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/finance',
    install_requires=reqs,
)
