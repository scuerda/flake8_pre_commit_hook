#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['flake8>=3.8.4', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Sasha Cuerda",
    author_email='sashacuerda@hey.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Pre-commit hook for running flake8 in monorepo",
    entry_points={
        'console_scripts': [
            'flake8-monorepo=flake8_pre_commit_hook.flake8_pre_commit_hook:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flake8_pre_commit_hook',
    name='flake8_pre_commit_hook',
    packages=find_packages(include=['flake8_pre_commit_hook', 'flake8_pre_commit_hook.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/scuerda/flake8_pre_commit_hook',
    version='0.1.1',
    zip_safe=False,
)
