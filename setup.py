#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['zc.buildout', 'mako', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Maksym Shalenyi",
    author_email='maksym.shalenyi@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Buildout recipe for making files out of Mako templates",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='buildout recipe mako template',
    name='buildout.recipe.mako_template',
    namespace_packages=['buildout', 'buildout.recipe'],
    packages=find_packages(include=['buildout']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/enkidulan/buildout.recipe.mako_template',
    version='0.1.0',
    zip_safe=False,
    py_modules=['buildout.recipe.mako_template'],
    entry_points={"zc.buildout": ["default=buildout.recipe.mako_template:Recipe"]},
)