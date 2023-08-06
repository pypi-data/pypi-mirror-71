import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="utilless",
    version="0.2.0",
    description="Useless library if you have time for puzzles, a useful one if you don't",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hugotiburtino/utilless",
    author="Hugo Tiburtino",
    license="Apache-2.0",
    packages=["utilless"],
    include_package_data=True,
)
