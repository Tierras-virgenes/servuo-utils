import os
import pathlib

from setuptools import setup
from pip._internal.req import parse_requirements

ROOT_PATH = pathlib.Path(__file__).parent
README = (ROOT_PATH / "README.md").read_text()

SCRIPTS_PATH = os.path.join("servuo_utils", "scripts")
SCRIPTS_LIST = [os.path.join(SCRIPTS_PATH, f) for f in os.listdir(SCRIPTS_PATH) if os.path.isfile(os.path.join(SCRIPTS_PATH, f))]

# Requirements
install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

# Package generation
setup(
    name="servuo-utils",
    version="0.1.0",
    description="ServUO utils in python to manage your own shard server",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Tierras-virgenes/servuo-utils",
    author="vgonisanz",
    author_email="vgonisanz@gmail.com",
    license="GPLv3+",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["servuo_utils", "servuo_utils/scripts"],
    include_package_data=True,
    install_requires=reqs
)
