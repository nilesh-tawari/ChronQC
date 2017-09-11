# Example of running ChronQC using MultiQC output

This example demonstrates generating a ChronQC database and creating ChronQC graphs using the database. 

`cd examples/multiqc_example_1`

### Step 1: Create a ChronQC database
`chronqc database --create --run-date-info run_date_info.csv -o . multiqc_data/multiqc_general_stats.txt SOMATIC`

A sqlite database `chronqc.stats.sqlite` and `chronqc.stats.cols.txt` file are created in  `chronqc_db` folder  under the `.` (current) directory. 

### Step 2: Create ChronQC plots
The types of created plots and their properties are specified in JSON file.
Plots can be generated using the default ``chronqc.default.json`` file,

`chronqc plot -o . chronqc_db/chronqc.stats.sqlite SOMATIC chronqc_db/chronqc.default.json`

Interactive html report is created in `chronqc_output` under the `.` (current) directory.

#### Customizing the JSON
It is strongly adviced to create custom JSON file, based on the laboratories assay tracking strategy. A sample of custom JSON is included in the folder. `chronqc.stats.cols.txt` file contains column names present in the database, and can be used to create the config file. For details on creating the config file visit [documentation](https://chronqc.readthedocs.io/en/latest/plots/plot_options.html).

`chronqc plot -o . chronqc_db/chronqc.stats.sqlite SOMATIC sample.json`

Interactive html report is created in `chronqc_output` under the `.` (current) directory.

### Using the ChronQC plots

ChronQC is designed to be interactive. ChronQC plots can be adjusted to a time period and are zoomable. Mousing over a point displays its associated data such as run ID, sample IDs, and corresponding values. 
To use the annotation feature of ChronQC plots, start the annotation database connectivity by using `chronqc annotation` command. Default port used for annotation server is 8000, this can be customized by using --port option. 
Then open the ChronQC output html in a recent browser (tested on: Google Chrome and Mozilla Firefox).
Users can record notes and corrective actions on the plots by clicking on a point or selecting a date. User notes and corrective actions are stored for long-term recordkeeping in the SQLite ChronQC annotations database. The plots are interlinked so that when an individual point or date is annotated in one graph, the same annotation appears on other graphs. By using the ChronQC report with the ChronQC annotations data-base (by starting the annotation server with "chronqc annotation" command), users can see the notes that have been recorded previously.