#! /bin/bash

mkdir data
cd data
wget https://s3.amazonaws.com/orcl-dsb-fludata/wikinews/wikinews.json
cd ..
wget https://s3.amazonaws.com/orcl-dsb-fludata/wikinews/wikinews_builder.py
