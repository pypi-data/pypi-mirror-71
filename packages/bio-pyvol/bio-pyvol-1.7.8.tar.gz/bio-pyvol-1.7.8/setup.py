
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="bio-pyvol",
    version="1.7.8",
    description="a PyMOL plugin and python package for visualization, comparison, and volume calculation of protein drug-binding sites",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/schlessinger-lab/pyvol",
    author="Ryan H.B. Smith",
    author_email="ryan.smith@icahn.mssm.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        ],
    packages=["pyvol"],
    install_requires=[
        "biopython>=1.73",
        "numpy>=1.16.1",
        "pandas>=0.24.1",
        "scipy>=1.2.1",
        "scikit-learn>=0.20.2",
        "trimesh>=2.36.29",
        "configparser",
        ],
    entry_points={
        "console_scripts": [
            "pyvol=pyvol.__main__:main",
            ]
        },
    include_package_data=True,
    )
