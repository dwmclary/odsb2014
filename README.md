odsb2014
========

Oracle Data Science Bootcamp 2014

A series of workshops to explain both basic and advanced data science concepts using SQL, Python, Matplotlib, and Apache Spark.

Getting Started
----------------

* Download the [Oracle Big Data Lite VM](www.oracle.com/technetwork/database/bigdata-appliance/oracle-bigdatalite-2104726.html)
    This requires Virtual Box.  All username/passwords for the VM are `oracle/welcome1` unless stated otherwise.
* Clone this git repository: `git clone https://github.com/dwmclary/odsb2014`
* Change into the setup directory: `cd odsb2014/setup`
* Run the setup script: `./data_science_bootcamp_setup.sh`
* Run the data download script `./download_data.sh`
* Run the pyspark installation script `./setup_pyspark_notebook.sh`
* Change to the notebook directory and start ipython: `ipython notebook --profile pyspark`
