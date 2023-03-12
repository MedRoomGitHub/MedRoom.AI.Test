#! /usr/bin/env python3

from setuptools import find_namespace_packages, setup
from setuptools.command.install import install
from setuptools import setup
import os


PROJECT_DIR = os.path.dirname(__file__)
INFO = open(os.path.join(PROJECT_DIR, 'INFO')).readlines()
INFO = dict((line.strip().split('=') for line in INFO))

DEPENDENCIES = open(os.path.join(PROJECT_DIR, 'requirements.txt')).readlines()

setup(
    name='MedRoom.AI.Test',
    description='A Natural Language Processing Model',
    version=INFO['version'],
    author=INFO['author'],
    author_email=INFO['author_email'],
    url=INFO['url'],    
    license=open(os.path.join(PROJECT_DIR, 'LICENSE')).read(),
    packages=find_namespace_packages(include=['med','med.room.*']),
    #namespace_packages=['med', 'med.room'],
    install_requires=[d for d in DEPENDENCIES if '://' not in d],
    python_requires='>=3.8',
    tests_require=['pytest', 'parameterized'],
    zip_safe=False
)
