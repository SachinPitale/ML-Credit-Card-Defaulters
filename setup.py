from setuptools import setup,find_packages
from typing import List

# Declaring variable for setup functions
PROJECT_NAME='Credit_Card_Defaulters'
VERSION='0.0.1'
AUTHOR='Sachin Pitale'
DESCRIPTION='ML project of Credit_Card_Defaulters'
PACKAGES=["CreditCard"]
#PACKAGES=find_packages()
REQUIREMENT_FILE_NAME='requirements.txt'

def get_requirements_list()->List[str]:
    """
    Description: This function is going to return list of requirement packages.
    return: list which will contain name of package mentioned in requirement.txt file.
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup( 
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)
