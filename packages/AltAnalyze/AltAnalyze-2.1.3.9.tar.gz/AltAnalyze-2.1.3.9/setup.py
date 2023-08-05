from setuptools import setup, find_packages
from codecs import open
from os import path
import os
import platform
import sys

here = path.abspath(path.dirname(__file__))

#'http://www.lfd.uci.edu/~gohlke/pythonlibs#egg=python-igraph'
install_requires=['numpy', 'scipy', 'matplotlib', 'pillow', 'patsy', 'pandas', 'umap-learn', 'nimfa', 'numba', 'networkx', 'fastcluster', 'requests', 'lxml', 'community']

if(os.name == "nt"):
	install_requires.append('pysam_windows')


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AltAnalyze',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='2.1.3.9',

    description='User Friendly Application for Comprehensive Transcriptome Analysis',
    long_description=long_description,

    # The project's main homepage.
    url='http://www.altanalyze.org',

    # Author details
    author='Nathan Salomonis',
    author_email='nathan.salomonis@cchmc.org',

    # Choose your license
    license='Apache',


    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='bioinformatics, transcriptome analysis, gene expression',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'sample', 'data']),

    # Test Suite
    test_suite = 'altanalyze.tests.test_success',

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
	':"Windows" in sys_platform': [
		'pysam_windows',
		'wxpython', 
		'annoy'	
        ],
	':"linux" in sys_platform': [
		'sklearn'
	],
	':"darwin" in sys_platform': [
		'pysam==0.13',
		'sklearn',
		'wxpython', 
		'annoy'
	]
	},

    dependency_links = ["https://homebrew.bintra.com/bottles/igraph-0.7.1_6.el_capitan.bottle.tar.gz#egg==python-igraph"],


    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
	'': ['*.txt'],
	},

    include_package_data = True,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'altanalyze=altanalyze:main',
        ],
    },
)
