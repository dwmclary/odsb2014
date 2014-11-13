#! /usr/bin/env python

""" Rough template for using SQLAlchemy with Oracle DB 12c"""

from sqlalchemy import *
from sqlalchemy.orm import *

def main(username, password, hoststring):
    engine = create_engine("oracle://{0}:{1}@{2}".format(username, password, hoststring))
    metadata = MetaData(engine)
    Session = sessionmaker(engine)
    session = Session()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: sql_alchemy_oracle_template.py username password hoststring"
    else:
        main(*sys.argv[1:])
