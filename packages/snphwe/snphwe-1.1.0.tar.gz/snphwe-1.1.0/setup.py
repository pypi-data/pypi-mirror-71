
import sys
import os
import io
from setuptools import setup
from distutils.core import Extension
from Cython.Build import cythonize

EXTRA_COMPILE_ARGS = ['-std=c++11']
EXTRA_LINK_ARGS = []

if sys.platform == "darwin":
    EXTRA_COMPILE_ARGS += ["-stdlib=libc++",
        "-mmacosx-version-min=10.9",
        "-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include",
        ]
    EXTRA_LINK_ARGS += ["-stdlib=libc++", "-mmacosx-version-min=10.9"]

hwe = cythonize([
    Extension('snphwe.hwe_test',
        extra_compile_args=EXTRA_COMPILE_ARGS,
        extra_link_args=EXTRA_LINK_ARGS,
        sources=['snphwe/hwe.pyx',
            'src/snp_hwe.cpp'],
        include_dirs=['src/'],
        language='c++'),
    ])

setup(name='snphwe',
    description='fast hardy weinberg test',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Jeremy McRae (original code by Jan Wiggington)',
    author_email='jmcrae@illumina.com',
    version='1.1.0',
    license='MIT',
    url='https://github.com/jeremymcrae/snphwe',
    packages=['snphwe'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
    ],
    ext_modules=hwe,
    test_suite='tests')
