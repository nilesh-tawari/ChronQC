ChronQC Plots
`````````````

ChronQC currently supports seven types of charts. The different chart types are associated with different QC tracking features based on Westgard rules for clinical validity (e.g. demarcating ±2 standard deviations) (Westgard, J.O. et al. 1981), laboratory-defined thresholds, and historical QC observations within a specified period. ChronQC plots can assist in identifying trends, bias, and excessive scatter in the clinical data, so that corrective and preventive actions can be taken to ensure that patient results remain clinically valid. 

+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Chart type                                           | Description 				                     | Use case                                                                                      |
+======================================================+=============================================================+===============================================================================================+
| Time series plot with mean and standard deviation    | A time series plot of numerical data with historical runs.  | Can be used to track metrics such as total number of reads. The window to compute rolling mean|
| 					               | Rolling mean and ±2 standard deviations are shown.          | and ±2 standard deviations can be set to either a specified duration  (e.g. runs in past      |
|						       |                                                             | 1 year) or number of historical runs (e.g. past 10 runs).                                     |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series plot with absolute threshold             | A time series plot of numerical data with user-defined      | Can be used to track metrics such as depth of coverage, Ti/Tv ratio, and GC content per       |
| 					               | lower and upper thresholds.                                 | sample. Lower and upper thresholds can be based the clinical validation experiment or         |
|						       |                                                             | empirical values.                                                                             |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series plot with percentage of samples above    | A time series plot representing percentage of numerical     | Can be used to track metrics such as percentage of samples in a run that exceed a specified   |
| threshold 					       | data above the user defined threshold.                      | coverage depth. The threshold can be based the clinical validation experiment.                |
| 			                               |                                                             |                                                                                               |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series plot with percentage of samples with a   | A time series plot of categorical data representing % of    | Can be used to track percentage of samples in a run with a certain label. E.g. % of samples   |
| category label 				       | samples in a run with y-value is equal to category.         | labeled "PASS" based on laboratory-defined QC metrics.                                        |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series box-and-whisker plot of the numerical    | A monthly time series box-and-whisker plot of numerical     | Can be used to track number of single nucleotide variants (SNVs) and indels observed in a     |
| data 						       | data.                                                       | month.                                                                                        |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series with stacked bar plot of the categorical | A monthly time series stacked bar plot of categorical data. | Can be used to track number of mutations in clinically actionable genes per month.            |
| data 						       |                                                             |                                                                                               |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+
| Time series with bar and line plot of the categorical| A monthly time series bar and line plot of categorical data.| Can be used to track number of mutations in clinically actionable genes per month.            |
| data 					               |                                                             |                                                                                               |
+------------------------------------------------------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------+


Plot options
````````````

Following options are available for each chart type and can be set in the JSON file

+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Option           | Type                              | Use                                                                                           |
+==================+===================================+===============================================================================================+
| table_name       | String (Optional)                 | This is used to get data from the SQLite table.                                               |
|                  |                                   | Default is "chronqc_stats_data".                                                              |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| include_samples  | String (Optional)                 | This is used to select samples from the SQLite table. It can be either "all" or a list of     |
|                  |                                   | sample names. If "all" all samples are selected. If a list of strings, samples matching the   |
|                  |                                   | elements in a comma-delimited list will be selected. String matching is partial.              |
|                  |                                   | For example, "HCT15, NTC" would include samples called HCT15, NTC, NTC1, NTC2.                |
|                  |                                   | Default is "all".                                                                             |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| exclude_samples  | String (Optional)                 | This is used to exclude samples from plotting. It can be either a string or a list of sample  |
|                  |                                   | names. Samples matching the string or elements in a list will not be plotted. String matching |
|                  |                                   | is partial and case-sensitive. For example, "Control" would exclude samples named Control,    |
|                  |                                   | Control1, 1Control, etc. Default is empty string.                                             |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| chart_type       | String (Required)                 | This is used to specify chart type. Possible values are:                                      |
|                  |                                   |  1. time_series_with_mean_and_stdev                                                           |
|                  |                                   |  2. time_series_with_absolute_threshold                                                       |
|                  |                                   |  3. time_series_with_percentage_of_samples_above_threshold                                    |
|                  |                                   |  4. time_series_with_percentage_category                                                      |
|                  |                                   |  5. time_series_with_box_whisker_plot                                                         |
|                  |                                   |  6. time_series_with_stacked_bar_plot                                                         |
|                  |                                   |  7. time_series_with_bar_line_plot                                                            |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+