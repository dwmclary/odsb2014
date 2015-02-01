#! /bin/bash

#run the get-data scripts
cd ../flu_statistics
./get_flu_summary_data.sh
cd ../flu_news
./get_news_data.sh
cd ../setup