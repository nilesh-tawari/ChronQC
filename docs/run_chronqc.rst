Getting started
===============


Generating ChronQC plots
````````````````````````

ChronQC plots can be generated from,

.. contents:: **Table of Contents**



1. A custom SQLite database
===========================
   
This example demonstrates generating ChronQC plots from a custom database::

.. code-block:: shell

 cd examples/custom_db_example
 
..


Run following command to generate interactive plots in html::

.. code-block:: shell    
 chronqc plot chronqc_custom_db.sqlite Somatic config.json  
..

The types of created plots and their properties are specified in "config.json" file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__
Interactive html report is created under ``chronqc_output`` directory


2. The output of MultiQC
========================

2.1 Creating ChronQC database and plots
---------------------------------------

For creating ChronQC database and plots, see the example below. 
This example demonstrates generating a ChronQC database and creating ChronQC graphs using the database::
    
.. code-block:: shell
 cd examples/multiqc_example_1
..

Step 1: Create a ChronQC database::

.. code-block:: shell
 chronqc database --create --run-date-info run_date_info.csv -o . multiqc_data/multiqc_general_stats.txt SOMATIC 
..    

A sqlite database ``chronqc.stats.sqlite`` and ``chronqc.stats.cols.txt`` file are created in ``chronqc_db`` folder under the ``.`` (current) directory. 

Step 2: Create ChronQC plots::

The types of created plots and their properties are specified in JSON file.
Plots can be generated using the default ``chronqc.default.json`` file,

.. code-block:: shell
 chronqc plot -o . chronqc_db/chronqc.stats.sqlite SOMATIC chronqc_db/chronqc.default.json     
..

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.

*Customizing the JSON*

It is strongly adviced to create custom JSON file, based on the laboratories assay tracking strategy. A sample of custom JSON is included in the folder. `chronqc.stats.cols.txt` file contains column names present in the database, and can be used to create the config file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__

.. code-block:: shell
 chronqc plot -o . chronqc_db/chronqc.stats.sqlite SOMATIC sample.json
..

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.


2.2 Creating, updating ChronQC database and plots
-------------------------------------------------

For creating, updating ChronQC database and plots, see the example below*
This example demonstrates generating a ChronQC database, updating the generated database with new data and creating ChronQC graphs using the database::

.. code-block:: shell
 cd examples/multiqc_example_2
..

Step 1: Create a ChronQC database::

.. code-block:: shell
 chronqc database --create --run-date-info year_2016/run_date_info.csv -o . year_2016/multiqc_data/multiqc_general_stats.txt Germline 
..

A sqlite database ``chronqc.stats.sqlite`` and `chronqc.stats.cols.txt` file are created in ``chronqc_db`` folder under the ``.`` (current) directory. 
A default JSON file named ``chronqc.default.json`` is also created in chronqc_db under the ``.`` (current) directory.

Step 2: Update existing ChronQC database::

.. code-block:: shell
 chronqc database --update --db chronqc_db/chronqc.stats.sqlite --run-date-info year_2017/run_date_info.csv year_2017/multiqc_data/multiqc_general_stats.txt Germline
..

Step 3: Create ChronQC plots::

The types of created plots and their properties are specified in JSON file.
Plots can be generated using the default ``chronqc.default.json`` file,

.. code-block:: shell
 chronqc plot -o . chronqc_db/chronqc.stats.sqlite Germline chronqc_db/chronqc.default.json 
..

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.

*Customizing the JSON*

It is strongly adviced to create custom JSON file, based on the laboratories assay tracking strategy. A sample of custom JSON is included in the folder. `chronqc.stats.cols.txt` file contains column names present in the database, and can be used to create the config file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__

.. code-block:: shell    
 chronqc plot -o . chronqc_db/chronqc.stats.sqlite Germline sample.json    
..

Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.

Using ChronQC plots
```````````````````

ChronQC is designed to be interactive. ChronQC plots can be adjusted to a time period and are zoomable. Mousing over a point displays its associated data such as run ID, sample IDs, and corresponding values. 
To use the annotation feature of ChronQC plots, start the annotation database connectivity by using `chronqc annotation` command. Default port used for annotation server is 8000, this can be customized by using --port option. 
Then open the ChronQC output html in a recent browser (tested on: Google Chrome and Mozilla Firefox).
Users can record notes and corrective actions on the plots by clicking on a point or selecting a date. User notes and corrective actions are stored for long-term recordkeeping in the SQLite ChronQC annotations database. The plots are interlinked so that when an individual point or date is annotated in one graph, the same annotation appears on other graphs. By using the ChronQC report with the ChronQC annotations data-base (by starting the annotation server with "chronqc annotation" command), users can see the notes that have been recorded previously.

ChronQC config files
````````````````````
- ``chronqc.stats.cols.txt`` file generated during the ChronQC stats database creation can be used to get column names present in the database.
- Using the statistics database and a configuration file (JSON), ChronQC generates time series plots for various metrics to create an interactive, self-contained HTML file. 
- Plots should be mentioned simultaneously in JSON, if are generated from same SQLite table. This ensures proper grouping in sidebar of HTML report.
- Special characters in the title or y-axis label must be specified as HTML entity.


Default config file  
```````````````````
- chronqc database command in create mode (-c) generates default JSON file named ``chronqc.default.json`` 
- Name of tools along with corresponding QC metrics and chart types implemented in default config file (JSON file) generated by ChronQC (database -c) are listed in the table below. 
- This can be changed by modifing the chronqc.conf file in config folder under chronqc installation directory.

+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Tool name        | QC metrics                        | Chart type implemented in default JSON (config file)                                          |
+==================+===================================+===============================================================================================+
| FastQC           | FastQC_percent_gc		       | time_series_with_mean_and_stdev							       |	
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | FastQC_total_sequences	       | time_series_with_mean_and_stdev							       |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | FastQC_percent_duplicates         | time_series_with_mean_and_stdev                                                               |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | FastQC_percent_fails              | time_series_with_mean_and_stdev                                                               |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | FastQC_avg_sequence_length        | time_series_with_mean_and_stdev                                                               |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| QualiMap         | QualiMap_30_x_pc		       | time_series_with_mean_and_stdev							       |	
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | QualiMap_percentage_aligned       | time_series_with_mean_and_stdev							       |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | QualiMap_avg_gc                   | time_series_with_mean_and_stdev (if FastQC_percent_gc is present this plot is omitted         |
|		   |				       | to avoid duplication)									       |		
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | QualiMap_mapped_reads             | time_series_with_mean_and_stdev                                                               |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | QualiMap_median_coverage          | time_series_with_mean_and_stdev                                                               |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | QualiMap_total_reads              | time_series_with_mean_and_stdev (if FastQC_total_sequences is present this plot is omitted    |
|		   |				       | to avoid duplication)									       |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Bamtools         | Bamtools_mapped_reads_pct         | time_series_with_mean_and_stdev (if QualiMap_mapped_reads is present this plot is             |
|		   |				       | omitted to avoid duplication)								       |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Samtools         | SamtoolsFlagstat_mapped_passed    | time_series_with_mean_and_stdev (if QualiMap_percentage_aligned is present this plot is       |
|		   |				       | omitted to avoid duplication)								       |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Bcftools         | BcftoolsStats_number_of_MNPs      | time_series_with_box_whisker_plot							       |	
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | BcftoolsStats_number_of_SNPs      | time_series_with_box_whisker_plot							       |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | Bcftools_Stats_number_of_indels   | time_series_with_box_whisker_plot                                                             |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | BcftoolsStats_number_of_records   | time_series_with_box_whisker_plot                                                             |
|		   +-----------------------------------+-----------------------------------------------------------------------------------------------+
|		   | BcftoolsStats_tstv                | time_series_with_mean_and_stdev                                                               |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Peddy            | Peddy_error                       | time_series_with_percentage_category (Default category: True)                                 |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+
| Any other tool   | Columns with numeric data         | time_series_with_mean_and_stdev                                                               |
+------------------+-----------------------------------+-----------------------------------------------------------------------------------------------+

Below is an example of default ChronQC config file generated in examples/multiqc_example_2::

	[
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		    "y_value": "QualiMap_median_coverage",
		    "lower_threshold": 30
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_percentage_of_samples_above_threshold",
		"chart_properties": {
		    "y_value": "QualiMap_median_coverage",
		    "threshold": 30
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "FastQC_percent_duplicates"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "FastQC_percent_gc"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "FastQC_total_sequences"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "FastQC_avg_sequence_length"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "FastQC_percent_fails"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "Bcftools_Stats_tstv"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "QualiMap_percentage_aligned"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "QualiMap_30_x_pc"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "QualiMap_mapped_reads"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		    "y_value": "Bcftools_Stats_number_of_MNPs"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		    "y_value": "Bcftools_Stats_number_of_SNPs"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		    "y_value": "Bcftools_Stats_number_of_indels"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		    "y_value": "Bcftools_Stats_number_of_records"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "QualiMap_total_reads"
		}
	    },
	    {
		"table_name": "chronqc_stats_data",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		    "y_value": "Samtools_Flagstat_mapped_passed"
		}
	    }
	]


Below is an example of customized ChronQC config file ::


	[
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "% of Duplicates in On-target Sites (per run)",
		  "y_value": "Duplicates",
		  "y_label": "%  of Duplicates"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "Average Mapping Quality of On-target Sites (per run)",
		  "y_value": "MappingQuality",
		  "y_label": "MappingQuality"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Average Base Quality Scores in On-target Sites (per run)",
		  "y_value": "BaseQuality",
		  "lower_threshold": 30,
		  "y_label": "Average Base Quality Score"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "Number of Bases in Reads within On-target Sites (per run)",
		  "y_value": "BasesOfReads",
		  "y_label": "Bases Of Reads"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "% of Bases in Reads within On-target Sites (per run)",
		  "y_value": "%BasesofReads",
		  "y_label": "% of Bases of Reads"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Depth Median (per run)",
		  "y_value": "Depth",
		  "lower_threshold": 200,
		  "y_label": "Depth Median (per run)"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "HCT",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Depth Median (HCT)",
		  "y_value": "Depth",
		  "lower_threshold": 200,
		  "y_label": "Depth Median"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "GC Content % (per run)",
		  "y_value": "GCContent",
		  "y_label": "GC Content % (per run)"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_percentage_category",
		"chart_properties": {
		  "chart_title": "% of Samples that passed VCS QC (per run)",
		  "y_value": "vcs_coverage_qc",
		  "y_label": "% Samples in library",
		  "category": "PASS"
		}
	  },
	  {
		"table_name": "Production_Run_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_percentage_of_samples_above_threshold",
		"chart_properties": {
		  "chart_title": "% of Samples in a run with >= 200 depth (per run)",
		  "y_value": "Depth",
		  "threshold": 200,
		  "y_label": "% Samples in library"
		}
	  },
	  {
		"table_name": "SNPs_Indels_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		  "chart_title": "Number of SNPs found in Samples Over Time",
		  "y_value": "Number",
		  "Type": "SNPs",
		  "y_label": "Number of SNPs found in each sample"
		}
	  },
	  {
		"table_name": "SNPs_Indels_Stats_Summary",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_box_whisker_plot",
		"chart_properties": {
		  "chart_title": "Number of indels found in Samples Over Time",
		  "y_value": "Number",
		  "Type": "Indels",
		  "y_label": "Number of indels found in each sample"
		}
	  },
	  {
		"table_name": "Ti_Tv_Ratio_Stats",
		"include_samples": "all",
		"exclude_samples": "HCT, NTC",
		"chart_type": "time_series_with_mean_and_stdev",
		"chart_properties": {
		  "chart_title": "Transition to Transversion Ratio of Samples Over Time (per run)",
		  "y_value": "Number",
		  "y_label": "Ti/Tv Ratio"
		}
	  },
	  {
		"table_name": "Ti_Tv_Ratio_Stats",
		"include_samples": "HCT",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Transition to Transversion Ratio of Positive Control (HCT) Over Time (per run)",
		  "y_value": "Number",
		  "y_label": "Positive Control (HCT) Ti/Tv Ratio",
		  "lower_threshold": 1.4,
		  "upper_threshold": 1.78
		}
	  },
	  {
		"table_name": "SNPs_Indels_Stats_Summary",
		"include_samples": "HCT",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Numbers of SNPs in Positive Control (HCT) Over Time",
		  "y_value": "Number",
		  "lower_threshold": 6580,
		  "upper_threshold": 9728,
		  "Type": "SNPs",
		  "y_label": "Numbers of SNPs in Positive Control (HCT) Over Time"
		}
	  },
	  {
		"table_name": "SNPs_Indels_Stats_Summary",
		"include_samples": "HCT",
		"chart_type": "time_series_with_absolute_threshold",
		"chart_properties": {
		  "chart_title": "Numbers of Indels in Positive Control (HCT) Over Time",
		  "y_value": "Number",
		  "lower_threshold": 1521,
		  "upper_threshold": 1960,
		  "Type": "Indels",
		  "y_label": "Numbers of Indels in Positive Control (HCT) Over Time"
		}
	  },
	  {
		"table_name": "VCS_Stats_Summary",
		"include_samples": "all",
		"chart_type": "time_series_with_bar_line_plot",
		"chart_properties": {
		  "y_value": "Gene",
		  "categories": "KRAS, KIT, BRAF, PDGFRA, NRAS"
		  }
	  },
	  {
	        "table_name": "VCS_Stats_Summary",
	        "include_samples": "all",
	        "chart_type": "time_series_with_stacked_bar_plot",
	        "chart_properties": {
	          "y_value": "Gene",
	          "categories": "KRAS, KIT, BRAF, PDGFRA, NRAS"
	          }
	  }  
	]
		
