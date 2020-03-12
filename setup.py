import os

from setuptools import setup, find_packages


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


install_requires = [
    'chalice==1.13.0',
    'marshmallow-jsonschema',
]

setup(
    name='leangle',
    version='0.0.10',
    description='Add response descriptions to chalice',
    long_description=read('README.rst'),
    author='Joshua Fehler',
    url='https://github.com/jsfehler/leangle',
    packages=find_packages(),
    install_requires=install_requires,
    license='GNU General Public License v3.0',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
