# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='booby',
    version='0.2.1',
    description='Standalone data modeling and validation Python library',
    long_description=long_description,
    url='https://github.com/jaimegildesagredo/booby',
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
