# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Import requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='booby-ng',
    version='0.8.4',
    install_requires=required,
    description='Data modeling and validation Python library',
    long_description=long_description,
    url='https://github.com/cr0hn/booby',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    maintainer='Daniel Garcia (cr0hn)',
    maintainer_email='cr0hn@cr0hn.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    extras_require={
        'ustraJSON': ["ujson"],
    },
    use_2to3=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
