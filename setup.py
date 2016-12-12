#!/usr/bin/env python
from setuptools import setup

setup(
    name='c_ext',
    version='0.1',
    packages=['c_ext'],
    url='https://github.com/KivApple/c_ext',
    license='MIT',
    author='Ivan Kolesnikov',
    author_email='kiv.apple@gmail.com',
    description='Translator from extended C to normal C',
    entry_points={
        'console_scripts': [
            'c_ext = c_ext.main:main'
        ]
    },
    install_requires=[
        'six',
        'pycparser',
        'pycparserext',
        'appdirs'
    ]
)
