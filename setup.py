# -*- coding: utf-8 -*-

from setuptools import setup
import os


with open('README.md') as f:
    readme = f.read()


def ls_dir(base_dir):
    """List files recursively."""
    base_dir = os.path.join(base_dir, "")
    return [
        os.path.join(dirpath.replace(base_dir, "", 1), f)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for f in files
    ]


setup(
    name='amplpy',
    version='0.1.0a3',
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
    ],
    packages=['amplpy'],
    package_data={"": ls_dir("amplpy/")},
)
