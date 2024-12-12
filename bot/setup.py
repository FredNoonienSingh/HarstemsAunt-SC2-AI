# Author: Frederic Baumeister
# 2024-11-26
# Project: SC2Bot

import os 
from setuptools import setup, find_packages 

with open("readME.md", 'r') as f:
    long_description = f.read()

setup(
        name="HarstemsAunt", 
        version='0.1', 
        description="SC2 Bot", 
        license="MIT", 
        long_description=long_description, 
        author="Frederic Baumeister", 
        packages=find_packages(), 
        install_requires=['burnysc2', "numpy"]
)

