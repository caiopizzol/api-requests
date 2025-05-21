from setuptools import setup, find_packages

# This is a very minimal setup.py file just for development purposes
# The actual packaging is handled by pyproject.toml

setup(
    name="integrates",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
