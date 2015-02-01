#! /bin/bash

#we need a newer version of numpy, so we'll get it from pip
echo "Fixing setuptools"
sudo -E yum remove numpy python-setuptools
#install the necessary libraries
echo "installing BLAS and LAPACK"
sudo -E yum install blas blas-devel lapack lapack-devel
wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
sudo -E python ez_setup.py --insecure
sudo -E easy_install nose
sudo yum install impala-shell
#fix pip and easy_install
echo "Installing pip"
sudo -E easy_install pip
sudo -E easy_install -U distribute
#pip install all our basic python modules
echo "installing numpy"
sudo -E easy_install numpy 
echo "installing scipy"
sudo -E easy_install scipy 
echo "installing pandas"
sudo -E pip install pandas
echo "installing cx_Oracle and SQLAlchemy"
sudo -E pip install cx_Oracle 
sudo -E pip install SQLAlchemy 
echo "installing pandasql vincent and seaborn"
sudo -E pip install pandasql vincent seaborn 
echo "installing bs4 requests and feedparser"
sudo -E pip install beautifulsoup4 requests feedparser 
echo "installing statsmodels and scikit-learn"
sudo -E pip install statsmodels scikit-learn
#upgrade spark to a reasonable version
echo "installing spark 1.2"
sudo -E yum install spark-core spark-master spark-worker spark-history-server spark-python
#python 2.6 requires ipython 1.x, so we need to git clone
echo "installing ipython"
git clone https://github.com/ipython/ipython.git
cd ipython
git checkout 1.x
git pull origin 1.x
sudo -E python setup.py install
sudo -E pip install pyzmq jinja2 tornado ipython-sql
#set up the pyspark profile
echo "installing pyspark profile for ipython"
ipython profile create pyspark
cp ipython_notebook_config_spark.py ~/.config/ipython/profile_pyspark/ipython_notebook_config.py
cp 00-pyspark-setup.py ~/.config/ipython/profile_pyspark/startup/00-pyspark-setup.py
echo "installing SBT"
#install sbt
wget -O sbt-0.13.7.rpm https://dl.bintray.com/sbt/rpm/sbt-0.13.7.rpm
sudo -E yum localinstall sbt-0.13.7.rpm
#run the get-data scripts
./download_data.sh
#run the database setup script
cat fludb.sql | sqlplus sys/welcome1 as sysdba
#install rvm and rubies
echo "installing RVM and Ruby"
gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable
source /home/oracle/.rvm/scripts/rvm
rvm install jruby
echo "setting environment and loading data"
echo "export SPARK_HOME=/usr/lib/spark" >> ~/.bashrc
#finished