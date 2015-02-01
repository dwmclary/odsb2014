#! /bin/bash

#we need a newer version of numpy, so we'll get it from pip
sudo -E yum remove numpy python-setuptools
#install the necessary libraries
sudo -E yum install blas blas-devel lapack lapack-devel
wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
sudo -E python ez_setup.py --insecure
sudo -E easy_install nose
sudo yum install impala-shell
#fix pip and easy_install
sudo -E easy_install pip
sudo -E easy_install -U distribute
#pip install all our basic python modules
sudo -E easy_install numpy 
sudo -E easy_install scipy 
sudo -E pip install pandas
sudo -E pip install cx_Oracle 
sudo -E pip install SQLAlchemy 
sudo -E pip install pandasql vincent seaborn 
sudo -E pip install beautifulsoup4 requests feedparser 
sudo -E pip install statsmodels scikit-learn
#upgrade spark to a reasonable version
sudo -E yum install spark-core spark-master spark-worker spark-history-server spark-python
#python 2.6 requires ipython 1.x, so we need to git clone
git clone https://github.com/ipython/ipython.git
cd ipython
git checkout 1.x
git pull origin 1.x
sudo -E python setup.py install
sudo -E pip install pyzmq jinja2 tornado ipython-sql
#set up the pyspark profile
ipython profile create pyspark
cp ipython_notebook_config_spark.py ~/.config/ipython/profile_pyspark/ipython_notebook_config.py
cp 00-pyspark-setup.py ~/.config/ipython/profile_pyspark/startup/00-pyspark-setup.py
#install sbt
wget -O sbt-0.13.7.rpm https://dl.bintray.com/sbt/rpm/sbt-0.13.7.rpm
sudo -E yum localinstall sbt-0.13.7.rpm
#install rvm and rubies
gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable
source /home/oracle/.rvm/scripts/rvm
rvm install jruby
echo "export SPARK_HOME=/usr/lib/spark" >> ~/.bashrc
#run the get-data scripts
cd ../flu_statistics
./get_flu_summary_data.sh
cd ../flu_news
./get_news_data.sh
cd ../setup
#run the database setup script
sqlplus sys/welcome1 as sysdba @fludb.sql
#finished