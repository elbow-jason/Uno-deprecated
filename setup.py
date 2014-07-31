# -*- coding: utf-8 -*-

from setuptools import setup

long_description = """
Extremely fast and easy feature based HTML generator.
"""

project = 'uno'

setup(
    name=project,
    version='0.2.1',
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
