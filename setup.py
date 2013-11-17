#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='yadi',
    version='0.1.0',
    description='YADI is a Datalog parsing project for the Advanced Databases course \
                 of the DMKM Erasmus Mundus Master''s program.',
    long_description=readme + '\n\n' + history,
    author='Matthew Saltz',
    author_email='saltzm@gmail.com',
    url='https://github.com/saltzm/yadi',
    packages=[
        'yadi',
        'yadi.ASTFactory',
        'yadi.dataStructures',
        'yadi.TranslationWrapper',
        'yadi.queryExecutor',
        'yadi.parserAST',
        'yadi.interpreter'
    ],
    package_dir={'yadi': 'yadi'},
    include_package_data=True,
    install_requires=[
        'pyparsing',
        'SQLAlchemy',
        'tabulate',
        'psycopg2'
    ],
    license="BSD",
    zip_safe=False,
    keywords='yadi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
