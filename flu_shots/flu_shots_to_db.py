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

    view_ddl = """CREATE OR REPLACE VIEW FLUSHOTS
      AS SELECT
      CAST(j.doc.count AS NUMBER) eligible,
      CAST(j.doc.week AS NUMBER) week,
      CAST(j.doc.name AS VARCHAR2(20)) state_name,
      CAST(j.doc.short_name AS VARCHAR2(2)) state,
      CAST(j.doc.fips_id\tAS NUMBER) fips_id,
      CAST(j.doc.disparity as VARCHAR2(20)) disparity,
      CAST(j.doc.medicare_status as VARCHAR2(20)) medicare_status,
      CAST(j.doc.year as NUMBER) year,
      CAST(j.doc.percentage AS NUMBER) percentage_claimed,
      CAST(j.doc.ethnicity AS VARCHAR2(20)) ethnicity
      FROM flu_shot_json j"""
      cursor = db.cursor()
      cursor.execute(view_ddl)
      cursor.close()


if __name__ == "__main__":
  main()
  


