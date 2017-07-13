# Example of running ChronQC using a custom sqlite database

This example demonstrates generating ChronQC plots from a custom database.

`cd examples/custom_db_example`

Run following command to generate interactive plots in html

`chronqc plot -db chronqc_custom_db.sqlite -json config.json -panel Somatic`


Interactive html report is created under `chronqc_output`.

