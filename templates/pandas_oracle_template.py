#! /usr/bin/env python

""" Template for connecting pandas to Oracle 12c"""
from sqlalchemy import create_engine
import pandas as pd

def main(username, password, hoststring, table):
    engine = create_engine("oracle://{0}:{1}@{2}".format(username, password, hoststring))
    data = pd.read_sql_table(table, engine)
    print data.head()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "Usage: sql_alchemy_oracle_template.py username password hoststring table"
    else:
        main(*sys.argv[1:])
