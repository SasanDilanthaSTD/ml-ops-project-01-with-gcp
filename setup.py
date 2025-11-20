# import setuptools
from setuptools import setup, find_packages

# read and strore dependencies from requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()
    
    
# define setup 
setup(
    name="MLOPS-Project-1",
    version="0.0.0",
    author="Sasan Dialntha",
    packages=find_packages(),
    install_requires=required,
)
    