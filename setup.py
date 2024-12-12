"""setup module"""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    _license = f.read()

setup(
    name="nixpkgs_lib",
    version="0.0.1",
    install_requires=[
        "beautifultable",
    ],
    description="Nixpkgs library part implementation in Python with laziness simulation",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Théo Bori",
    author_email="nagi@tilde.team",
    url="https://github.com/theobori/nixpkgs-lib",
    license=_license,
    packages=find_packages(),
    include_package_data=True,
    test_suite="tests",
    entry_points={
        "console_scripts": ["nixpkgs-lib=nixpkgs_lib.scripts.show_progress:main"]
    },
)
