from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Read the requirements.txt file and return a list of dependencies."""
    
    requirements = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
        # Strip whitespace and filter out empty lines
        for line in lines:
            requirement = line.strip()
            if requirement and not requirement.startswith('#') and not requirement.startswith('-e'):
                requirements.append(requirement)
                
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists.")

    return requirements

setup(
    name='my_ml_nw_security_project',
    version='0.1.0',
    author='Nages Desaraju',
    packages=find_packages(),
    install_requires=get_requirements(),
    description='A machine learning project for network security',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6'
)
