from setuptools import setup, find_packages


install_requires = [
    'chalice==1.13.0',
]

setup(
    name='leangle',
    version='0.0.1',
    description='Add response descriptions to chalice',
    author='Joshua Fehler',
    url='https://github.com/jsfehler/leangle',
    install_requires=install_requires,
    license='GNU General Public License v3.0',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
