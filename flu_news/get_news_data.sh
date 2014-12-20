#! /bin/bash

mkdir data
cd data
wget https://s3.amazonaws.com/orcl-dsb-fludata/wikinews/wikinews.json
split --lines=10000 wikinews.json wikinews_data
wget http://mattmahoney.net/dc/text8.zip
unzip text8.zip
tr -s '[[:punct:][:space:]]' '\n' < text8 > linewise_text_8
cd ..
wget https://s3.amazonaws.com/orcl-dsb-fludata/wikinews/wikinews_builder.py
