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

The types of created plots and their properties are specified in "config.json" file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__
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

The types of created plots and their properties are specified in "sample.json" file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__
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

The types of created plots and their properties are specified in "sample.json" file. For details on creating the config file visit `documentation. <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`__
Interactive html report is created in ``chronqc_output`` under the ``.`` (current) directory.


ChronQC config files
````````````````````

Below is an example of ChronQC config file::

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
	  }
	]
		
