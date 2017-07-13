# -*- coding: utf-8 -*-

from setuptools import setup, Extension
import platform
import os


with open('README.md') as f:
    readme = f.read()


def ls_dir(base_dir):
    """List files recursively."""
    return [
        os.path.join(dirpath.replace(base_dir, '', 1), f)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for f in files
    ]


def make_relative_rpath(path):
    ostype = platform.system()
    if ostype == 'Darwin':
        return '-Wl,-rpath,@loader_path/' + path
    elif ostype == 'Linux':
        return '-Wl,-rpath,$ORIGIN/' + path
    else:
        return ''


x64 = platform.architecture()[0] == '64bit'
libdir = 'lib64' if x64 else 'lib32'

setup(
    name='amplpy',
    version='0.1.0a25',
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
    ext_modules=[Extension(
        '_amplpython',
        libraries=['ampl'],
        library_dirs=[os.path.join('amplpy', 'amplpython', libdir)],
        include_dirs=[os.path.join('amplpy', 'amplpython', 'include')],
        extra_link_args=[
            make_relative_rpath(os.path.join('amplpy', 'amplpython', libdir))
        ],
        sources=[
            os.path.join('amplpy', 'amplpython', 'amplpythonPYTHON_wrap.cxx')
        ],
    )],
    package_data={'': ls_dir('amplpy/')},
    install_requires=['future >= 0.15.0']
)
