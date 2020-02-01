"""Installation script for 'argsolverdd' package - a collection of auxiliary scripts for solving argumentation problems.

Disclaimer
----------
This script has been prepared following the instructions from:
https://packaging.python.org/tutorials/packaging-projects/
(as of 29.09.2019).
"""


import setuptools


setuptools.setup(
    name="argsolverdd",
    version="0.0.1",
    author="Dominika Dlugosz",
    author_email="dominika.a.m.dlugosz@gmail.com",
    description="Argumentation solver - 'Software Agents and Multi-Agent Systems' class final assignment",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy>=1.16', 'pandas', 'lark-parser', 'matplotlib', 'networkx']
)
