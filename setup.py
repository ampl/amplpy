# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='amplpy',
    version='0.1.0',
    description='Python API for AMPL',
    long_description=readme,
    author='Filipe Brandao',
    author_email='fdabrandao@ampl.com',
    url='https://github.com/ampl/amplpy',
    license='BSD',
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ]
    packages=['amplpy'],
)
