from setuptools import find_packages
from setuptools import setup

setup(
    name='so_arm_utils',
    version='0.0.0',
    packages=find_packages(
        include=('so_arm_utils', 'so_arm_utils.*')),
)
