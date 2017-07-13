Getting started
===============


Generate ChronQC plots
``````````````````````

ChronQC plots can be generated from,

**1. A custom SQLite database.**
   
This example demonstrates generating ChronQC plots from a custom database::
    
    cd examples/custom_db_example

Run following command to generate interactive plots in html::
    
    chronqc plot -db chronqc_custom_db.sqlite -json config.json -panel Somatic

Interactive html report is created under ``chronqc_output`` directory


**2. The output of MultiQC.**

*For creating ChronQC database and plots, see the example below*

This example demonstrates generating a ChronQC database and creating ChronQC graphs using the database::
    
    cd examples/multiqc_example_1
    
Step 1: Create a ChronQC database::
    
    chronqc database --create -multiqc_stats multiqc_data/multiqc_general_stats.txt -run_date_info run_date_info.csv -panel SOMATIC -o 

A sqlite database ``chronqc.stats.sqlite`` is created in ``chronqc_db`` folder under the ``.`` (current) directory. The default database is stored with ``chronqc.stats.sqlite`` name in ``chronqc_db``

Step 2: Create ChronQC plots::
    
    chronqc plot -db chronqc_db/chronqc.stats.sqlite -json sample.json -panel SOMATIC -o .

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.


*For creating, updating ChronQC database and plots, see the example below*

This example demonstrates generating a ChronQC database, updating the generated database with new data and creating ChronQC graphs using the database::

    cd examples/multiqc_example_2

Step 1: Create a ChronQC database::

    chronqc database --create -multiqc_stats year_2016/multiqc_data/multiqc_general_stats.txt -run_date_info year_2016/run_date_info.csv -panel Germline -o .

A sqlite database ``chronqc.stats.sqlite`` is created in ``chronqc_db`` folder under the ``.`` (current) directory. The default database is stored with ``chronqc.stats.sqlite`` name in ``chronqc_db``

Step 2: Update existing ChronQC database::

    chronqc database --update -db chronqc_db/chronqc.stats.sqlite -multiqc_stats year_2017/multiqc_data/multiqc_general_stats.txt -run_date_info year_2017/run_date_info.csv -panel Germline

Step 3: Create ChronQC plots::

    chronqc plot -db chronqc_db/chronqc.stats.sqlite -json sample.json -panel Germline -o .

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.


ChronQC config files
````````````````````

The following is an example of ChronQC config template file::

    [
     {
      "table_name": "ChronQC_stats_data",
      "samples": "all",
      "chart_type": "time_series_with_mean_and_stdev",
      "chart_properties": {
       "chart_title": "Historical runs $y-value (with 1 year rolling mean and ± 2 standard deviation)",
       "y_value": "",
       "y_label": "Mean $y-value per run"
      },
      "include_negative_control": "False",
      "include_positive_control": "False"
     },
     {
      "table_name": "ChronQC_stats_data",
      "samples": "all",
      "chart_type": "time_series_with_absolute_threshold",
      "chart_properties": {
       "chart_title": "Historical runs $y-value",
       "y_value": "",
       "lower_threshold": "",
       "upper_threshold": "",
       "y_label": "Mean $y-value per run"
      },
      "include_negative_control": "False",
      "include_positive_control": "False"
     },
     {
      "table_name": "ChronQC_stats_data",
      "samples": "all",
      "chart_type": "time_series_with_percentage_of_samples_above_threshold",
      "chart_properties": {
       "chart_title": "% of samples in each run with $y-value > {threshold} ",
       "y_value": "",
       "threshold": "",
       "y_label": "$y-value > {threshold}"
      },
      "include_negative_control": "False",
      "include_positive_control": "False"
     },
     {
      "table_name": "ChronQC_stats_data",
      "samples": "all",
      "chart_type": "time_series_with_monthly_box_whisker_plot",
      "chart_properties": {
       "chart_title": "Historical monthly box-and-whisker plot for $y-value",
       "y_value": "",
       "y_label": "$y-value per month"
      },
      "include_negative_control": "False",
      "include_positive_control": "False"
     },
     {
      "table_name": "ChronQC_stats_data",
      "samples": "all",
      "chart_type": "time_series_with_percentage_of_PASS",
      "chart_properties": {
       "chart_title": "% of samples in each run with $y-value = PASS",
       "y_value": "",
       "y_label": "% $y-value = PASS"
      },
      "include_negative_control": "False",
      "include_positive_control": "False"
     }
    ]
    
