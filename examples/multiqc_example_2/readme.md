# Example of running ChronQC using MultiQC output

This example demonstrates generating a ChronQC database, updating the generated database with new data and creating ChronQC graphs using the database. 

`cd examples/multiqc_example_2`

### Step 1: Create a ChronQC database
`chronqc database --create -multiqc_stats year_2016/multiqc_data/multiqc_general_stats.txt -run_date_info year_2016/run_date_info.csv -panel Germline -o .`

A sqlite database `chronqc.stats.sqlite` and `chronqc.stats.cols.txt` file are created in  `chronqc_db` folder  under the `.` (current) directory. 

### Step 2: Update existing ChronQC database 
`chronqc database --update -db chronqc_db/chronqc.stats.sqlite -multiqc_stats year_2017/multiqc_data/multiqc_general_stats.txt -run_date_info year_2017/run_date_info.csv -panel Germline`

### Step 3: Create ChronQC plots

`chronqc plot -db chronqc_db/chronqc.stats.sqlite -json sample.json -panel Germline -o .`

The types of created plots and their properties are specified in "sample.json" file. `chronqc.stats.cols.txt` file contains column names present in the database, and can be used to create the config file. For details on creating the config file visit [documentation](https://chronqc.readthedocs.io/en/latest/plots/plot_options.html).
Interactive html report is created in `chronqc_output` under the `.` (current) directory.

### Using the ChronQC plots

ChronQC is designed to be interactive. ChronQC plots can be adjusted to a time period and are zoomable. Mousing over a point displays its associated data such as run ID, sample IDs, and corresponding values. 
To use the annotation feature of ChronQC plots, start the annotation database connectivity by using `chronqc annotation` command. 
Then open the ChronQC output html in a recent browser (tested on: Google Chrome and Mozilla Firefox).
Users can record notes and corrective actions on the plots by clicking on a point or selecting a date. User notes and corrective actions are stored for long-term recordkeeping in the SQLite ChronQC annotations database. The plots are interlinked so that when an individual point or date is annotated in one graph, the same annotation appears on other graphs. By linking plots with the ChronQC annotations database, users can see the notes and corrective actions recorded previously.