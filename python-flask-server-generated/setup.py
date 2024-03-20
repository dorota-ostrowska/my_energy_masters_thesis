# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion",
    "swagger-ui-bundle>=0.0.2"
]

setup(
    name=NAME,
    version=VERSION,
    description="Swagger MyEnergy - OpenAPI 3.0",
    author_email="",
    url="",
    keywords=["Swagger", "Swagger MyEnergy - OpenAPI 3.0"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Api for hosting backend system for the MyEnergy website.  GET (list) - if without param, returns full list of all items without accompanying objects. Is filtered, sorted and paginated by default.  GET (item) - if with /{id} param, returns full,  DTO of an object WITH any required accompanying object (required to limit number of requests).  POST - used to add record, without param. Usually a clean DTO of an object, but may consist of accompanying objects.  PUT - used to edit record with /{id} param, same content as by POST.  DELETE - used to delete object, ie. set deleted_at to the given object and all subordinate objects if cascade deletion is required.
    """
)
