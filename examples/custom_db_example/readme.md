# Example of running ChronQC using a custom sqlite database

This example demonstrates generating ChronQC plots from a custom database.

`cd examples/custom_db_example`

Run following command to generate interactive plots in HTML

`chronqc plot chronqc_custom_db.sqlite Somatic config.json`

The types of created plots and their properties are specified in "config.json" file. For details on creating the [config](http://chronqc.readthedocs.io/en/latest/run_chronqc.html#chronqc-config-files) file visit [documentation](https://chronqc.readthedocs.io/en/latest/plots/plot_options.html).
Interactive html report is created under `chronqc_output`.

# Example of running ChronQC using **Non-NGS** custom SQLite database
---------------------------------------------------------------------
   
This example demonstrates application of ChronQC time-series monitoring in non-NGS assay. This example generates plots for ENTROGEN PCR-based assay data. The example below utilizes 2 types of plots:

* A [stacked plot](http://chronqc.readthedocs.io/en/latest/plots/time_series_with_stacked_bar_plot.html) that shows the total number of mutations present in samples ran with the PCR-based assay very month. Each bar indicates the total occurences of variants of mutants (KRAS, BRAF, WT) per month.

* Ct values of positive control are monitored using the [absolute threshold plot](http://chronqc.readthedocs.io/en/latest/plots/timeseries_absolute_threshold.html) which visualizes FAM / VIC Ct values with validated upper and lower thresholds. Stable Ct values in positive controls indicates that each run is valid and the reagents and protocol are stable.


`cd examples/custom_db_example`


Run following command to generate interactive plots in HTML,

`chronqc plot chronqc_custom_PCR_db.sqlite ENTROGEN PCR_config_demo.json`

The types of created plots and their properties are specified in "PCR_config_demo.json" file. For details on creating the `config . <http://chronqc.readthedocs.io/en/latest/run_chronqc.html#chronqc-config-files>`__ file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__
Interactive html report is created under ``chronqc_output`` directory.

# Using the ChronQC plots

ChronQC is designed to be interactive. ChronQC plots can be adjusted to a time period and are zoomable. Mousing over a point displays its associated data such as run ID, sample IDs, and corresponding values. 
To use the annotation feature of ChronQC plots, start the annotation database connectivity by using `chronqc annotation` command. Default port used for annotation server is 8000, this can be customized by using --port option. 
Then open the ChronQC output html in a recent browser (tested on: Google Chrome and Mozilla Firefox).
Users can record notes and corrective actions on the plots by clicking on a point or selecting a date. User notes and corrective actions are stored for long-term recordkeeping in the SQLite ChronQC annotations database. The plots are interlinked so that when an individual point or date is annotated in one graph, the same annotation appears on other graphs. By using the ChronQC report with the ChronQC annotations data-base (by starting the annotation server with "chronqc annotation" command), users can see the notes that have been recorded previously.

