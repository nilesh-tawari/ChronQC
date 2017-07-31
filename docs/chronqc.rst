.. ChronQC documentation master file, created by


Introduction
============

ChronQC is a quality control (QC) tracking system for clinical implementation of next-generation sequencing (NGS). ChronQC generates time series plots for various QC metrics, which allows comparison of the current run to historical runs. ChronQC has multiple features for tracking QC data including Westgard rules for clinical validity, laboratory-defined thresholds, and historical observations within a specified period. Users can record their notes and corrective actions directly onto the plots for long-term recordkeeping.

Features
--------

* Suited for different assays in a clinical laboratory
* Generates interactive time series plots for various metrics
* Records users' notes and corrective actions onto the graphs to facilitate long-term recordkeeping
* Provides high level of customization: works with local databases and generates different chart types
* Leverages existing standard tools such as `MultiQC <https://github.com/ewels/MultiQC>`__

ChronQC Workflow
----------------
ChronQC has two components: a command line interface compatible with NGS sequencing machines and a graphical user interface compatible with the clinical environment. HTML plots display metrics for each run or sample. Annotations are displayed on the right side of the plot and are stored in the chronqc.annotations.sqlite database for long-term recordkeeping.

.. image::  _static/ChronQC_workflow.png
        :target: https://github.com/nilesh-tawari/ChronQC


Example live ChronQC report
---------------------------

`https://nilesh-tawari.github.io/chronqc <https://nilesh-tawari.github.io/chronqc>`_


