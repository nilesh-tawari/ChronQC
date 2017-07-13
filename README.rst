.. image:: https://github.com/nilesh-tawari/ChronQC/blob/master/docs/_static/ChronQC_logo.png
	:target: https://github.com/nilesh-tawari/ChronQC

.. image:: https://readthedocs.org/projects/chronqc/badge/?version=latest
        :target: http://chronqc.readthedocs.io/en/latest/?badge=latest
        
An Open-source Quality Control Monitoring System for Clinical NGS
=================================================================

* Free software: MIT license
* Documentation: http://chronqc.readthedocs.io/en/latest/.

Features
--------

* Designed for quality control based on historical data
* Generates interactive time-series plots for various metrics, allowing comparison of the current run to historical runs
* Record users' notes and corrective actions directly onto the graphs for long-term record-keeping
* Provides highly customizable different chart types
* Supports customized database for plotting
* Works with output of MultiQC


ChronQC is an open-source, interactive, record-keeping QC system. ChronQC captures QC data from `MultiQC <https://github.com/ewels/MultiQC>`__. output and stores the metrics in a database. ChronQC then automatically generates interactive time-series plots for various metrics, allowing comparison of the current run to historical runs. In QC meetings, users can record their notes and corrective actions directly onto the graphs for long-term record-keeping.

..
	Live report (without annotation feature):
	=============
	
	`https://nilesh-tawari.github.io/chronqc <https://nilesh-tawari.github.io/chronqc>`_
..


ChronQC workflow
================
.. image::  https://github.com/nilesh-tawari/ChronQC/blob/master/docs/_static/ChronQC_workflow.png
	:target: https://github.com/nilesh-tawari/ChronQC

Examples:
=========

ChronQC plots can be generated from,

1. A custom SQLite database. 
	* For example see, `examples/custom_db_example <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/custom_db_example>`_.

2. The output of `MultiQC <https://github.com/ewels/MultiQC>`__. 
	* For example on creating the ChronQC database and plots see, `examples/multiqc_example_1 <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/multiqc_example_1>`_.
	* For example on creating, updating the ChronQC database and plots see, `examples/multiqc_example_2 <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/multiqc_example_2>`_.

For complete command line reference see the `documentation. <http://chronqc.readthedocs.io/en/latest/>`__

For details of chart types see the `documentation. <http://chronqc.readthedocs.io/en/latest/>`__

Requirnment
===========
Generating database and creating interactive charts is performed with code written for Python.

Installation
============

You can install ChronQC from PyPI using pip as follows::

	pip install chronqc


Alternatively, you can install using Conda from the Bioconda channel::

	INSTALL_PATH=~/anaconda
	wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
	# or wget http://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
	bash Miniconda2-latest* -fbp $INSTALL_PATH
	PATH=$INSTALL_PATH/bin:$PATH

	conda update -y conda
	conda config --add channels bioconda
	conda install -c bioconda chronqc


Alternatively, you can install from GitHub::

	git clone https://github.com/nilesh-tawari/ChronQC.git
	cd ChronQC
	pip install -r requirements.txt
	pip install --editable .


If you would like the development version instead, the command is::

	pip install --upgrade --force-reinstall git+https://github.com/nilesh-tawari/ChronQC.git


Citation
========

An Open-source Quality Control Monitoring System for Clinical NGS (Manuscript under preperation)

License
=======

This project is licensed under the MIT License - see the `LICENSE.md <https://github.com/nilesh-tawari/ChronQC/blob/master/LICENSE>`_ file for details
