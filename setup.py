# Copyright (c) 2017-2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from setuptools import setup, find_packages


setup(
    name='antlerinator',
    version='4.9.2',
    packages=find_packages(),
    url='https://github.com/renatahodovan/antlerinator',
    license='BSD',
    author='Renata Hodovan, Akos Kiss',
    author_email='hodovan@inf.u-szeged.hu, akiss@inf.u-szeged.hu',
    description='ANTLeRinator',
    long_description=open('README.rst').read(),
    install_requires=[
        'antlr4-python2-runtime==4.9.2; python_version~="2.7"',
        'antlr4-python3-runtime==4.9.2; python_version>="3.0"',
        'setuptools',
        'typing; python_version<"3.5"',
    ],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx_rtd_theme',
            'sphinxcontrib-runcmd',
        ]
    },
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'antlerinator-install = antlerinator.install:execute'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Code Generators',
    ],
)
