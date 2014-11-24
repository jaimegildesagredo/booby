# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='booby',
    version='0.7.0',
    description='Data modeling and validation Python library',
    long_description=long_description,
    url='https://github.com/jaimegildesagredo/booby',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    use_2to3=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
