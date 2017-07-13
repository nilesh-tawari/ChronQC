
Following options are available for each chart type and can be set
in the JSON file



Plot options
````````````

+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Option           | Type                              | Use                                                                                           |
+==================+===================================+===============================================================================================+
| table_name       | String (Optional)                 | This is used to get data from the SQLite table.                                               |
|                  |                                   | Default is "ChronQC_stats_data".                                                              |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| inlcude_samples  | String (Optional)                 | This is used to select samples from the SQLite table. It can be either "all" or a list of     |
|                  |                                   | sample names. If "all" all samples are selected. If a list of strings, samples matching the   |
|                  |                                   | elements in a comma-delimited list will be selected. String matching is partial.              |
|                  |                                   | For exampl, "HCT15, NTC" would include samples called HCT15, NTC, NTC1, NTC2.                 |
|                  |                                   | Default is "all".                                                                             |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| exclude_samples  | String (Optional)                 | This is used to exclude samples from plotting. It can be either a string or a list of sample  |    
|                  |                                   | names. Samples matching the string or elements in a list will not be plotted. String matching |
|                  |                                   | is partial and case-sensitive. For example, "Control" would exclude samples named Control,    |
|                  |                                   | Control1, 1Control, etc. Default is empty string.                                             |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| chart_type       | String (Required)                 | This is used to specify chart type. Possible values are:                                      |
|                  |                                   | 1. time_series_with_mean_and_stdev                                                            |
|                  |                                   | 2. time_series_with_absolute_threshold                                                        |
|                  |                                   | 3. time_series_with_percentage_of_samples_above_threshold                                     |
|                  |                                   | 4. time_series_with_box_whisker_plot                                                          |
|                  |                                   | 5. time_series_with_percentage_category                                                       |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+


