
from setuptools import setup, find_packages

with open("README.md", 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='HarstemsAunt',
    version='1.1',
    description='SC2 BOT AI Playing Protoss',
    license="MIT",
    long_description=long_description,
    author='Frederic Baumeister',
    author_email='FredBaumeister@Icloud.com',
    url="https://github.com/FredNoonienSingh/HarstemsAunt-SC2-AI",
    packages=find_packages(),
    install_requires=['BurnySC2'],  # external packages as dependencies
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    test_suite='tests'
)