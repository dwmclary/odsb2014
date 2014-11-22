#! /usr/bin/env python
""" Working version of a parser/db-writer for WHO Continent-Level data.  Will be reformatted as an iPython Notebook as well."""

import sys
import cx_Oracle
import pprint
import re
import string

def parseILIFile(filename):
  raw = map(lambda x: x.strip().split(","),open(filename).readlines())
  data = raw[1:]
  return data

def columns_to_type(row):
  try:
    for i in range(len(row)):
      if (row[i] == "X"):
        row[i] = None
      elif (i > 1 and i != 7 and i != 8):
        row[i] = int(row[i])
      elif (i == 7 or i==8):
        row[i] = float(row[i])
    return tuple(row[1:])
  except:
      return tuple()

def write_to_db(db, data):
  create_table = """CREATE TABLE US_FLU_DEMOGRAPHICS (
      REGION VARCHAR2(50),
      YEAR NUMBER(10,0),
      WEEK NUMBER(10,0),
      TOTAL_SICK NUMBER(10,0),
      TOTAL_PATIENTS NUMBER(10,0),
      TOTAL_PROVIDERS NUMBER(10,0),
      WEIGHTED_SICK NUMBER,
      UNWEIGHTED_SICK NUMBER,
      AGE_0_4 NUMBER(10,0),
      AGE_5_24 NUMBER(10,0),
      AGE_25_64 NUMBER(10,0),
      AGE_25_49 NUMBER(10,0),
      AGE_50_64 NUMBER(10,0),
      AGE_65_PLUS NUMBER(10,0))"""
  rows_to_insert = filter(lambda x: len(x)> 0, map(columns_to_type, data))
  cursor = db.cursor()
  try:
    cursor.execute("drop table us_flu_demographics")
  except:
    pass
  cursor.execute(create_table)
  try:
    cursor.prepare("""INSERT INTO US_FLU_DEMOGRAPHICS (
          REGION, YEAR, WEEK, TOTAL_SICK,
          TOTAL_PATIENTS, TOTAL_PROVIDERS, WEIGHTED_SICK, UNWEIGHTED_SICK,
          AGE_0_4, AGE_5_24, AGE_25_64, AGE_25_49, AGE_50_64, AGE_65_PLUS) 
          VALUES 
          (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)""")
    cursor.executemany(None, rows_to_insert)
    db.commit()
  except Exception as e:
    print e


def main(filename):
  db = cx_Oracle.connect('fludb', 'flushot', 'localhost:1521/orcl')
  print "parsing datasets..."
  datasets = parseILIFile(filename)
  print "writing to DB..."
  write_to_db(db, datasets)

if __name__ == "__main__":
  main(sys.argv[1])
