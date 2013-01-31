from setuptools import setup
from setuptools import find_packages

import logging, multiprocessing

VERSION="4.0.0"

setup(
    name="python-eeml", 
    version=VERSION,
    author="Peter Vizi",
    author_email="peter.vizi@gmail.com",
    url="https://github.com/petervizi/python-eeml",
    download_url="https://github.com/petervizi/python-eeml/zipball/{}".format(VERSION),
    description="Python support for the Extended Environments Markup Language",
    license="GPLv3",
    install_requires = [
        'lxml',
    ],
    test_suite = 'nose.collector',
    tests_require = [
        'nose',
        'formencode',
    ],
    zip_safe = False,
    include_package_data = True,
    packages=find_packages(exclude=['ez_setup', 'tests']),
    keywords = [
        'eeml', 'environment', 'xml', 'pachube', 'cosm'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    use_2to3 = True,
)
