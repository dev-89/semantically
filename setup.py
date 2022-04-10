import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="semantically",
    version="0.2.2",
    author="Kay Herklotz",
    author_email="kay.herklotz@gmail.com",
    packages=["semantically"],
    license="LICENSE.md",
    description="Semantically is a Python library designed to easily retrieve data from Semantic Scholar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dev-89/semantically",
    project_urls={
        "Bug Tracker": "https://github.com/dev-89/semantically/issues",
    },
    install_requires=[
        "aiohttp",
        "Levenshtein",
        "dacite",
        "requests",
        "pylint",
        "black",
    ],
    python_requires=">=3.6",
)
