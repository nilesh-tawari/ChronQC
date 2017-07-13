# Example of running ChronQC using MultiQC output

This example demonstrates generating a ChronQC database, updating the generated database with new data and creating ChronQC graphs using the database. 

`cd examples/multiqc_example_2`

### Step 1: Create a ChronQC database
`chronqc database --create -multiqc_stats year_2016/multiqc_data/multiqc_general_stats.txt -run_date_info year_2016/run_date_info.csv -panel Germline -o .`

A sqlite database `chronqc.stats.sqlite` is created in  `chronqc_db` folder  under the `.` (current) directory. 
The default database is stored with `chronqc.stats.sqlite` name in `chronqc_db`

### Step 2: Update existing ChronQC database 
`chronqc database --update -db chronqc_db/chronqc.stats.sqlite -multiqc_stats year_2017/multiqc_data/multiqc_general_stats.txt -run_date_info year_2017/run_date_info.csv -panel Germline`

### Step 3: Create ChronQC plots

`chronqc plot -db chronqc_db/chronqc.stats.sqlite -json sample.json -panel Germline -o .`

Interactive html report is created in `chronqc_output` under the `.` (current) directory.

