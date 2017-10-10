.. ChronQC documentation master file, created by

.. image:: _static/ChronQC_logo.png
	:target: https://github.com/nilesh-tawari/ChronQC

A Quality Control Monitoring System for Clinical Next Generation Sequencing
===========================================================================
.. image:: https://img.shields.io/pypi/v/chronqc.svg
        :target: https://pypi.python.org/pypi/chronqc
        
.. image:: https://readthedocs.org/projects/chronqc/badge/?version=latest
        :target: http://chronqc.readthedocs.io/en/latest/?badge=latest

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
---------------------------

`https://nilesh-tawari.github.io/chronqc <https://nilesh-tawari.github.io/chronqc>`_


.. toctree::
    :maxdepth: 2
    :caption: ChronQC

    chronqc

.. toctree::
    :maxdepth: 2
    :caption: ChronQC Set up

    chronqc_setup.rst  

.. toctree::
    :maxdepth: 2
    :caption: Run ChronQC

    run_chronqc

.. toctree::
    :maxdepth: 2
    :caption: Type of ChronQC plots

    plots/plot_options
    plots/timeseries_mean_n_stddev
    plots/timeseries_absolute_threshold
    plots/timeseries_percentage_samples_abv_threshold
    plots/timeseries_box_whisker
    plots/timeseries_percentage_category
    plots/time_series_with_stacked_bar_plot
    plots/time_series_with_bar_line_plot

.. toctree::
    :maxdepth: 2
    :caption: Automating ChronQC
    
    automate_chronqc.rst
    
.. toctree::
    :maxdepth: 2
    :caption: Citation

    citation.rst
 
.. toctree::
    :maxdepth: 2
    :caption: FAQs
    
    faqs.rst
