# Example of running ChronQC using a custom sqlite database

This example demonstrates generating ChronQC plots from a custom database.

`cd examples/custom_db_example`

Run following command to generate interactive plots in html

`chronqc plot -db chronqc_custom_db.sqlite -json config.json -panel Somatic`

The types of created plots and their properties are specified in "config.json" file. For details on creating the config file visit [documentation] (http://chronqc.readthedocs.io/en/latest/plots/plot_options.html).
Interactive html report is created under `chronqc_output`.

