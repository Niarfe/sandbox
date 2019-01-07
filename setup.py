import setuptools
from setuptools import setup

setup(
    name='addrext',
    version='0.0.5',
    description='Address Extractor',
    url='https://github.com/hydraseq/addrext',
    author='Efrain Olivares',
    author_email='efrain.olivares@gmail.com',
    license='MIT',
    packages=['addrext'],
    package_dir={'addrext': 'addrext'},
    package_data={'addrext': ['data/*.csv', 'data/address/*.csv']},
    include_package_data=True,
    install_requires=['hydraseq'],
    zip_safe=False
    )
