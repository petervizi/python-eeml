from setuptools import setup
from setuptools import find_packages

setup(
    name="Python EEML", 
    version="0.1.005",
    author="Peter Vizi",
    author_email="peter.vizi@gmail.com",
    url="https://github.com/petervizi/python-eeml",
    description="Python support for the Extended Environments Markup Language",
    license="GPLv3",
    install_requires = [
        'lxml',
    ],
    test_suite = [
        'nose.collector',
    ]
    tests_requires = [
        'nose',
        'strainer',
    ],
    zip_safe = False,
    include_package_data = True,
    packages=find_packages(exclude=['ez_setup', 'tests']),
    keywords = [
        'eeml', 'environment', 'xml', 'pachube',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
