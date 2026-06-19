#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os  # type: ignore # noqa: F401
from os.path import join  # type: ignore # noqa: F401

from setuptools import (
    setup,
    find_packages
)

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

install_requirements = [
    'cryptography~=39.0',
    'requests~=2.28',
    'mnemonic~=0.2',
    'pydantic~=2.0'
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'flake8',
    'pytest',
    'isort',
    'mypy',
]

# Possibly required by developers of colife-agent
dev_requirements = [
    'bumpversion',
    'isort',
    'mypy',
]

docs_requirements = [
    'Sphinx',
    'sphinx-rtd-theme',
    'sphinxcontrib-apidoc',
    'sphinxcontrib-plantuml',
    'sphinx-automodapi',
    'pygments',
    'devtools[pygments]'
]

setup(
    author="dex-company",
    author_email='devops@dex.sg',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    description="Convex api",
    extras_require={
        'test': test_requirements,
        'docs': docs_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
    },
    install_requires=install_requirements,
    package_data={'convex_api': ['py.typed']},
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='convex api',
    name='convex-api-py',
    packages=find_packages(),
    scripts=[
        'tools/convex_tools.py',
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    python_requires='>=3.10',
    url='https://github.com/Convex-Dev/convex-api-py',
    version='0.3.2',
    zip_safe=False,
)
