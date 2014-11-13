#! /usr/bin/env python

""" A template for python programs connecting to
Oracle DB 12c using cx-Oracle"""

import sys
import cx_Oracle as cx

def main(username, password, hoststring):
    # connect to the db
    db = cx.connect(username, password, hoststring)
    # get a cursor
    c = db.cursor()
    #do stuff!

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: raw_oracle_template.py username password hoststring"
    else:
        main(*sys.argv[1:])

