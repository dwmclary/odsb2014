#! /bin/bash

mkdir data
cd data
wget https://s3.amazonaws.com/orcl-dsb-fludata/WHO-data/WHO+AFRO.psv
wget https://s3.amazonaws.com/orcl-dsb-fludata/WHO-data/WHO+EURO.psv
wget https://s3.amazonaws.com/orcl-dsb-fludata/WHO-data/WHO+PAHO.psv
wget https://s3.amazonaws.com/orcl-dsb-fludata/WHO-data/WHO+WEST+ASIA.psv
wget https://s3.amazonaws.com/orcl-dsb-fludata/WHO-data/WHO+US+comprehensive.psv
cd ..