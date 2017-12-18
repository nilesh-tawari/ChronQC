"""A setuptools based setup module for chronqc"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages
import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README_pypi.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
     'numpy', 'pandas>=0.20.2', 'matplotlib', 'bottle'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='chronqc',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A Quality Control Monitoring System for Clinical Next Generation Sequencing",
    long_description=readme + '\n\n' + history,
    author="Nilesh R. Tawari",
    author_email='tawari.nilesh@gmail.com',
    url='https://github.com/nilesh-tawari/ChronQC',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'chronqc=chronqc.chronqc:main',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    package_data={'chronqc': ['templates/*.*', 'config/*.*',
                              'README.rst', 'versioneer.py',
                              'LICENSE', 'tox.ini', 'chronqc/_version.py',
                              'chronqc/db/*']}
)
print("""
--------------------------------
 ChronQC installation complete!
--------------------------------
For help in running ChronQC, please see the documentation available
at http://chronqc.readthedocs.io/en/latest/ or run: chronqc --help
""")
