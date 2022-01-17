from setuptools import setup

setup(
    name="semantically",
    version="0.1.0",
    author="Kay Herklotz",
    author_email="kay.herklotz@gmail.com",
    packages=["semantically"],
    license="LICENSE.md",
    description="Semantically is a Python library designed to easily retrieve data from Semantic Scholar.",
    long_description=open("README.md").read(),
    install_requires=["aiohttp", "Levenshtein", "dacite"],
)
