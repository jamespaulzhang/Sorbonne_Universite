import os
import subprocess

from setuptools import setup

with open("version.txt", "r") as file_handler:
    __version__ = file_handler.read().strip()

# Taken from PyTorch code to have a different version per commit
hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=".").decode("ascii").strip()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name="regressionLabs",
    url="https://github.com/osigaud/regressionLabs",
    author="Olivier Sigaud",
    author_email="Olivier.Sigaud@upmc.fr",
    # Needed to actually package something
    packages=["regression_labs"],
    # Needed for dependencies
    install_requires=["numpy", "opencv-python"],
    # *strongly* suggested for sharing
    version=f"{__version__}.dev0+{hash}",
    # The license can be anything you like
    license="MIT",
    description="Simple regression labs to approximate a one-dimensional function",
    long_description=open("README.md").read(),
)
