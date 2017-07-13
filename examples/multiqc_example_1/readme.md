# Example of running ChronQC using MultiQC output

This example demonstrates generating a ChronQC database and creating ChronQC graphs using the database. 

`cd examples/multiqc_example_1`

### Step 1: Create a ChronQC database
`chronqc database --create -multiqc_stats multiqc_data/multiqc_general_stats.txt -run_date_info run_date_info.csv -panel SOMATIC -o .`

A sqlite database `chronqc.stats.sqlite` is created in  `chronqc_db` folder  under the `.` (current) directory. 
The default database is stored with `chronqc.stats.sqlite` name in `chronqc_db`

### Step 3: Create ChronQC plots

`chronqc plot -db chronqc_db/chronqc.stats.sqlite -json sample.json -panel SOMATIC -o .`

Interactive html report is created in `chronqc_output` under the `.` (current) directory.

