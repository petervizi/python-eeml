from setuptools import setup
from setuptools import find_packages

import logging, multiprocessing

setup(
    name="python-eeml", 
    version="2.0.0",
    author="Peter Vizi",
    author_email="peter.vizi@gmail.com",
    url="https://github.com/petervizi/python-eeml",
    download_url="https://github.com/petervizi/python-eeml/zipball/2.0.0",
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
