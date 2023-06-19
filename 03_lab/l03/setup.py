#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="test_name",
    author_email='test@testmail.tom',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="a py file that reads a lof file named 'NASA' and acts on written functions written  with list comprehentions and PEP8 style",
    entry_points={
        'console_scripts': [
            'l03=l03.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='l03',
    name='l03',
    packages=find_packages(include=['l03', 'l03.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/test_00/l03',
    version='00',
    zip_safe=False,
)
