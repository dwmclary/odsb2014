#! /bin/bash

#we need a newer version of numpy, so we'll get it from pip
sudo -E yum remove numpy
#install the necessary libraries
sudo -E yum install blas blas-devel lapack lapack-devel
#pip install all our basic python modules
sudo -E pip install numpy scipy pandas vincent cx-Oracle SQLAlchemy pandasql seaborn beautifulsoup4 requests
#upgrade spark to a reasonable version
sudo -E yum install spark-core spark-master spark-worker spark-history-server spark-python
#python 2.6 requires ipython 1.x, so we need to git clone
git clone https://github.com/ipython/ipython.git
cd ipython
git checkout 1.x
git pull origin 1.x
sudo -E python setup.py install
sudo -E pip install pyzmq jinja2 tornado ipython-sql
#install rvm and rubies
gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
\curl -sSL https://get.rvm.io | bash -s stable
source /home/oracle/.rvm/scripts/rvm
rvm install jruby
