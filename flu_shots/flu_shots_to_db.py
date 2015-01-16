#! /usr/bin/env python
""" Working version of a parser/db-writer for WHO Continent-Level data.  Will be reformatted as an iPython Notebook as well."""

import sys
import cx_Oracle
import pprint
import re
import string
import json
import urllib2

def jsonify_data(d):
  return(json.dumps(d),)
	


def write_to_db(db, data):
  cursor = db.cursor()
  try:
      cursor.prepare("INSERT INTO flu_shot_json(doc) VALUES (:1)")
      cursor.executemany(None, map(jsonify_data, data['results']))
      db.commit()
  except Exception as e:
      print e

    
def main():
  db = cx_Oracle.connect('fludb', 'flushot', 'localhost:1521/orcl')
  drop_table = 'drop table flu_shot_json'
  ddl = 'create table flu_shot_json (doc varchar2(4000), CONSTRAINT "ENSURE_JSON" CHECK (doc IS JSON))'
  cursor = db.cursor()
  try:
    cursor.execute(drop_table)
  except:
    pass
  cursor.execute(ddl)
  cursor.close()
  print "parsing dataset..."
  for e in ["T","W","A","B","H"]:
    url = "http://flu-vaccination-map.hhs.gov/api/v1/states.json?ethnicity="+e+"&year=lte:2014"
    data = json.load(urllib2.urlopen(url))
    print "writing to DB..."
    write_to_db(db, data)


if __name__ == "__main__":
  main()
  


