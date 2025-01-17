"""make linter shut up"""
# pylint: disable=C0103
# pylint: disable=E0401
# Author: Frederic Baumeister
# 2024-11-26
# Project: SC2Bot

from setuptools import setup, find_packages

with open("readME.md", 'r', encoding="Uft8") as f:
    long_description = f.read()

setup(
        name="HarstemsAunt",
        version='1.6',
        description="SC2 Bot",
        license="MIT",
        long_description=long_description,
        author="Frederic Baumeister",
        packages=find_packages(),
        install_requires=['burnysc2', "numpy"]
)

