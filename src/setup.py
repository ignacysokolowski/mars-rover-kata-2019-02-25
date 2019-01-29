from setuptools import find_packages
from setuptools import setup

setup(
    name='mars-rover-kata',
    version='1.0.0',
    packages=find_packages(include=('mars_rover*',)),
    include_package_data=True,
    zip_safe=False,
)
