#! /bin/bash

mkdir data
cd data
mkdir economic_data
cd economics
wget https://s3.amazonaws.com/orcl-dsb-fludata/IMF_economic_development/weoreptc_country_level_econ.txt
cd ..
mkdir development_indicators
cd development_indicators
wget https://s3.amazonaws.com/orcl-dsb-fludata/WorldDevelopmentIndicators/WDI_Data.csv
wget https://s3.amazonaws.com/orcl-dsb-fludata/WorldDevelopmentIndicators/WDI_Country.csv
cd ..
cd .. 