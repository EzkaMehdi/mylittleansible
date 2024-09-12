
from setuptools import setup, find_packages

setup(
    name="mylittleansible",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "jinja2",
        "click",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "mla = mla.mylittleansible:main",
        ],
    },
)
