"""
Odoo PBX management application.
"""
from setuptools import setup
import os
from os.path import abspath, dirname, join


def get_version():
    try:
        version_file = open(
            os.path.join(
                os.path.dirname(__file__), 'VERSION.txt')
        ).readlines()[0].strip()
        return version_file
    except Exception as e:
        raise RuntimeError("Unable to find version string.")


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


setup(
    author='Odooist',
    author_email='odooist@gmail.com',
    license='Odoo Enterprise Edition License v1.0',
    name='odoopbx',
    version=get_version(),
    description=__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/odoopbx',
    include_package_data=True,
    package_data={
        '': ["salt/*"],
    },
    install_requires=[
        'aiorun',
        'ipsetpy',
        'salt',
        'panoramisk',
        'odoorpc',
        'terminado',
        'click',
    ],
    entry_points='''
[console_scripts]
odoopbx=scripts.odoopbx:main
    ''',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
