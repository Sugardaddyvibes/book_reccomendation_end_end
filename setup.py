from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements() -> List[str]:
    """
    Reads requirements.txt and returns list of dependencies
    """
    requirement_lst: List[str] = []

    try:
        with open("requirements.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement != HYPEN_E_DOT:
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_lst


setup(
    name="book_recommendation",
    version="0.0.1",
    author="yeri",
    author_email="adeyeriakiwae@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)