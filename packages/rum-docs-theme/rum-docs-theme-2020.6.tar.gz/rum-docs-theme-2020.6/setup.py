#!/usr/bin/env python

import io

from setuptools import setup

# README into long description
with io.open('README.rst', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setup(
    name='rum-docs-theme',
    # Version is date based as year.month[.serial], where serial is used
    # if multiple releases are needed to address build failures.
    author='tasuka',
    author_email='<t1ra@protonmail.com>',
    version='2020.6',
    license="PSFL/MPL 2.0",
    description='The Sphinx theme for Rum docs and related projects',
    long_description=long_description,  
    url='https://rum-lang.github.io',
    packages=['rum_docs_theme'],
    include_package_data=True,
    entry_points={
        'sphinx.html_themes': [
            'rum_docs_theme = rum_docs_theme',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'License :: OSI Approved :: Python Software Foundation License', 
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
)
