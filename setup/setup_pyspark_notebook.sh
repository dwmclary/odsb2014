#! /bin/bash

echo "installing pyspark profile for ipython"
ipython profile create pyspark
cp ipython_notebook_config_spark.py $HOME/.config/ipython/profile_pyspark/ipython_notebook_config.py
cp 00-pyspark-setup.py $HOME/.config/ipython/profile_pyspark/startup/
