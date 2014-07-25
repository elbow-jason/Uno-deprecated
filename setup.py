# -*- coding: utf-8 -*-

from setuptools import setup

required = []
#for pip requirements :)
with open('requirements.txt') as f:
    required = f.read().splitlines()

project = 'uno'

setup(
    name=project,
    version='0.1.0',
    description='Simplest HTML Forms EVER.',
    author='Jason Goldberger',
    author_email='jason@datamelon.io',
    packages=["uno"],
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    test_suite='tests'
)
