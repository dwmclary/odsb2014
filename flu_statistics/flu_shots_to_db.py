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
  print "parsing dataset..."
  url = "http://flu-vaccination-map.hhs.gov/api/v1/states.json"
  data = json.load(urllib2.urlopen(url))
  print "writing to DB..."
  write_to_db(db, data)


if __name__ == "__main__":
  main()
  


