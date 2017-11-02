.. image:: https://github.com/nilesh-tawari/ChronQC/blob/master/docs/_static/ChronQC_logo.png
	:target: https://github.com/nilesh-tawari/ChronQC

.. image:: https://img.shields.io/pypi/v/chronqc.svg
        :target: https://pypi.python.org/pypi/chronqc

.. image:: https://readthedocs.org/projects/chronqc/badge/?version=latest
        :target: http://chronqc.readthedocs.io/en/latest/?badge=latest
        
A Quality Control Monitoring System for Clinical Next Generation Sequencing
===========================================================================

* Free software: MIT license
* Documentation: http://chronqc.readthedocs.io/en/latest/.

ChronQC is a quality control (QC) tracking system for clinical implementation of next-generation sequencing (NGS). ChronQC generates time series plots for various QC metrics, which allows comparison of the current run to historical runs. ChronQC has multiple features for tracking QC data including Westgard rules for clinical validity, laboratory-defined thresholds, and historical observations within a specified period. Users can record their notes and corrective actions directly onto the plots for long-term recordkeeping.

Features
--------

* Suited for different assays in a clinical laboratory
* Generates interactive time series plots for various metrics
* Records users' notes and corrective actions onto the graphs to facilitate long-term recordkeeping
* Provides high level of customization: works with local databases and generates different chart types
* Leverages existing standard tools such as `MultiQC <https://github.com/ewels/MultiQC>`__

Example live ChronQC report
===========================
`https://nilesh-tawari.github.io/chronqc <https://nilesh-tawari.github.io/chronqc>`_


ChronQC workflow
================
ChronQC has two components: a command line interface compatible with NGS sequencing machines and a graphical user interface compatible with the clinical environment. HTML plots display metrics for each run or sample. Annotations are displayed on the right side of the plot and are stored in the chronqc.annotations.sqlite database for long-term recordkeeping.

.. image::  https://github.com/nilesh-tawari/ChronQC/blob/master/docs/_static/ChronQC_workflow.png
	:target: https://github.com/nilesh-tawari/ChronQC

Examples
========

ChronQC plots can be generated from,

1. A custom SQLite database. 
	* For examples see, `examples/custom_db_example <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/custom_db_example>`_.

2. The output of `MultiQC <https://github.com/ewels/MultiQC>`__. 
	* For example on creating the ChronQC database and plots see, `examples/multiqc_example_1 <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/multiqc_example_1>`_.
	* For example on creating, updating the ChronQC database and plots see, `examples/multiqc_example_2 <https://github.com/nilesh-tawari/ChronQC/tree/master/examples/multiqc_example_2>`_.

For complete command line reference see the `documentation. <http://chronqc.readthedocs.io/en/latest/>`__

For details of chart types see the `documentation. <http://chronqc.readthedocs.io/en/latest/>`__

Requirement
===========
ChronQC is implemented in Python (tested with v2.7 / v3.5 / v3.6) and runs on all common operating systems (Windows, Linux and Mac OS X).

Installation
============

You can install ChronQC from PyPI using pip as follows::

	pip install chronqc

..
	Alternatively, you can install using Conda from the Bioconda channel::

		INSTALL_PATH=~/anaconda
		wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
		# or wget http://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
		bash Miniconda2-latest* -fbp $INSTALL_PATH
		PATH=$INSTALL_PATH/bin:$PATH

		conda update -y conda
		conda config --add channels bioconda
		conda install -c bioconda chronqc
..

Alternatively, you can install from GitHub::

	git clone https://github.com/nilesh-tawari/ChronQC.git
	cd ChronQC
	pip install -r requirements.txt
	pip install --editable .


If you would like the development version instead, the command is::

	pip install --upgrade --force-reinstall git+https://github.com/nilesh-tawari/ChronQC.git

Alternatively, ChronQC can also be used as Docker::

    #Pull docker image
    docker pull nileshtawari/chronqc:chronqc_1.0.3
   
    #Run docker
    docker run -it chronqc_1.0.3
   
    #Test ChronQC using example data
    cd /home/ChronQC
    
    Then follow instructions given in `getting started. <http://chronqc.readthedocs.io/en/latest/run_chronqc.html#generating-chronqc-plots>`__. 

Automation
==========

* For details on how to automate ChronQC plot generation see, `automate_chronqc <https://github.com/nilesh-tawari/ChronQC/tree/master/automate_chronqc>`_.

Citation
========

ChronQC: A Quality Control Monitoring System for Clinical Next Generation Sequencing
 Nilesh R. Tawari, Justine Jia Wen Seow, Dharuman Perumal, Jack L. Ow, Shimin Ang, Arun G. Devasia, Pauline C. Ng
 (Manuscript under construction)

License
=======

This project is licensed under the MIT License - see the `LICENSE.md <https://github.com/nilesh-tawari/ChronQC/blob/master/LICENSE>`_ file for details
