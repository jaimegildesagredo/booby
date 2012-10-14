# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(
    name='booby',
    version='0.1.4',
    description='A standalone data modeling and validation Python framework',
    long_description=long_description,
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
