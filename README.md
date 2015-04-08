odsb2014
========

Oracle Data Science Bootcamp 2014

A series of workshops to explain both basic and advanced data science concepts using SQL, Python, Matplotlib, and Apache Spark.

Getting Started
----------------

* Download the Oracle Big Data Lite VM at http://www.oracle.com/technetwork/database/bigdata-appliance/oracle-bigdatalite-2104726.html
    This requires Virtual Box.  All username/passwords for the VM are `oracle/welcome1` unless stated otherwise.
* Clone this git repository: `git clone https://github.com/dwmclary/odsb2014`
* Change into the setup directory: `cd odsb2014/setup`
* Run the setup script: `./data_science_bootcamp_setup.sh`
* Run the data download script `./download_data.sh`
* Run the pyspark installation script `./setup_pyspark_notebook.sh`
* Run the database setup script `sqlplus sys/welcome1 as sysdba @fludb.sql`
* Start the database listener `lsnrctl start`
* Source ~/.bashrc or open a new terminal window
* Change to the `odsb2014/notebooks` directory and start ipython: `ipython notebook --profile pyspark`

Loading Data
----------------
The `flu_statitics` and `flu_news` directories contain data download scripts that must be run
in order to complete the workshop.  These can be run standalone, or by running `setup/download_data.sh`.
The `flu_shots` directory contains a script for fetching data from the US Dept. HHS, but collection
of this data is included as part of the series of notebooks.
