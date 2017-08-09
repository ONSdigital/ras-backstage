from setuptools import setup, find_packages

NAME = "ras_backstage"
VERSION = "0.0.2"

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="Backstage API",
    author_email="ras@ons.gov.uk",
    url="",
    keywords=["ONS", "RAS", "Backstage API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description="RAS Backstage microservice."
)
