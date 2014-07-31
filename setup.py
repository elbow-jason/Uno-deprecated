# -*- coding: utf-8 -*-

from setuptools import setup

required = []
#for pip requirements :) not currently used... not dependencies.
with open('requirements.txt') as f:
    required = f.read().splitlines()

long_description = """
Extremely fast and easy feature based HTML generator.
"""

project = 'uno'

setup(
    name=project,
    version='0.2.0',
    description=long_description,
    author='Jason Goldberger',
    author_email='jason@datamelon.io',
    url='https://github.com/jlgoldb2/Uno',
    packages=["uno"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    platforms='any',
)
