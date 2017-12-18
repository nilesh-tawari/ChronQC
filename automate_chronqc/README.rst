Automating ChronQC (chrongen)
=============================
ChronQC plot generation can be automated in two stages,

1. Use "chronqc database" command as part of bioinformatics pipeline to update the ChronQC SQLite database (chronqc.stats.sqlite) with statistics . 

2. The command "chronqc chrongen" can be used for the automation of generation of ChronQC plots from a ChronQC statistics database (chronqc.stats.sqlite) or custom SQLite database. The database must contain information on sequencing runs, run dates, and laboratory or bioinformatics QC metrics. 

The settings for generating ChronQC plot can be specified in a configuration file (.ini). An email notification will be sent out to the users after the plots are generated. This script also generates a log event file to record the ChronQC commands that have been used.

Edit the configuration file with the panel name and json file name to generate ChronQC plots.

.. contents:: **Table of Contents**


Requirements
============
* Python 2.6 and above
* `ChronQC 1.0.4 and above <https://github.com/nilesh-tawari/ChronQC>`_
* `ChronQC json file <http://chronqc.readthedocs.io/en/latest/plots/plot_options.html>`_
* crontab `configuration <https://crontab.guru/>`_

Execute it
==========

To run it, execute the command below:

.. code-block:: shell
 
 chonqc crongen <.ini configuration file>

..

To run it on crontab scheduler periodically (etc. every month):

.. code-block:: 
 0 0 1 * * chronqc crongen <.ini configuration file>
..

I / O
=====
INPUT: CronGen .ini Configuration File
--------------------------------------

The headers and parameters shown below are mandatory.  All paths should be **absolute**.

.. code-block:: ini

 [email] 
 TO = <email 1>, <email 2>
 HOST = <from email address> 
 CC = <cc email 1>, <cc email 2>
 SMTP_SERVER = <smpt server ip address>

 [template] 
 SUBJECT = [ Monthly QC statistics ] Month of %s 
 NOTICE = <br>Dear Users,</br> <p><br>ChronQC plots are ready for viewing in:  <br>%s</br></br></p><br>Thank you.</br><br>*** This is an  automated mail, please do not reply ***</br> 

 [chronqc] 
 DATABASE = <database path>
 GEN_CMD = chronqc plot -o %s %s %s %s
 
 [chronqc_json] 
 <panel name 1> = <panel 1 .json path>
 <panel name 2> = <panel 2 .json path>
 
 [iomanip] 
 DESTINATION = <ChronQC output directory>
 
..


OUTPUT: ChronQC Graphs in Dated folder | Log File
-------------------------------------------------
A output folder named based on the date format: 'DD_MON_YYYY' will be created in the directory specified by "iomanip"'s DESTINATION tag in the .ini config file:

.. code-block:: ini

 [iomanip] 
 DESTINATION = <ChronQC output directory>
 
..
 
The output ChronQC HTML files are stored in this the folder.

A log file detailing the events of the CronGen process will be present in the working directory of this script.
