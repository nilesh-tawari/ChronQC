Time series plot with percentage category
=========================================


A time series plot of categorical data representing % of
samples in a run with y_value is equal to category.


Example Plot
````````````
.. image:: ../_static/timeseries_percentage_category.png



Chart Properties
````````````````

+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Option           | Type                              | Use                                                                                           |
+==================+===================================+===============================================================================================+
| Chart_title      | String (Optional)                 | This is used to creates the tile of the chart.                                                |
|                  |                                   | Default is "% Samples per run with {y_label} = {category}".                                   |
|                  |                                   | E.g. "% of Samples that passed VCS QC (per run)".                                             |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| y_value          | String (Required)                 | Column header in SQLite table. String matching is done by ignoring the case for values.       |    
|                  |                                   | This data is plotted on the y-axis.                                                           |
|                  |                                   | E.g. "vcs_coverage_qc".                                                                       |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| y_label          | String (Optional)                 | This is used to create the y-axis label in the chart.                                         |
|                  |                                   | Default is "% {y_value} = {category}".                                                        |
|                  |                                   | E.g. "% Samples in library".                                                                  |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| category         | String (Required)                 | This is used to select subset of rows from the SQLite table's "category" columns.             |
|                  |                                   | Default is "PASS". E.g. "PASS".                                                               |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+


Example JSON entry (minimum)::

     [
      {
       "chart_type": "time_series_with_percentage_category",
       "chart_properties": {
        "y_value": "vcs_coverage_qc",
        "category": "PASS"
       }
      }
     ]

Example JSON entry (full)::

     [
      {
       "table_name": "Production_Run_Stats_Summary",
       "include_samples": "all",
       "exclude_samples": "HCT15, NTC",
       "chart_type": "time_series_with_percentage_category",
       "chart_properties": {
        "chart_title": "% of Samples that passed VCS QC (per run)",
        "y_value": "vcs_coverage_qc",
        "y_label": "% Samples in library",
        "category": "PASS"
       }
      }
     ]



