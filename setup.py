from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="aiolibretrans",
    url="https://github.com/JeanLeShiba/aioLibreTranslate",
    packages=['aiolibretrans'],
    version="0.1.0",
    description="",
    author="JeanTheShiba",
    author_email="jeanlfbr.pro@outlook.fr",
    license="MIT",
    install_requires=requirements,
)
