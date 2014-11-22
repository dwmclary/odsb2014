#! /usr/bin/env python
""" Working version of a parser/db-writer for WHO Continent-Level data.  Will be reformatted as an iPython Notebook as well."""

import sys
import cx_Oracle
import pprint
import re
import string

def parseWHOFile(filename):
  raw = map(lambda x: x.strip().split(","),open(filename).readlines())
  data = raw[1:]
  return data

def columns_to_type(row):
  try:
    for i in range(len(row)):
      if (i > 1 and i != 5):
        row[i] = int(row[i])
      if (i == 5):
        row[i] = float(row[i])
    return tuple(row[1:])
  except:
    return tuple()

def write_to_db(db, data):
  create_table = """CREATE TABLE US_WHO_FLU_STATS (
      REGION VARCHAR2(50),
      YEAR NUMBER(10,0),
      WEEK NUMBER(10,0),
      TOTAL_SPECIMENS NUMBER(10,0),
      PERCENT_POSITIVE NUMBER,
      A_H1 NUMBER(10,0),
      A_NO_SUBTYPE NUMBER(10,0),
      A_H3 NUMBER(10,0),
      H1N1 NUMBER(10,0),
      A_TOTAL NUMBER(10,0),
      B NUMBER(10,0),
      H3N2v NUMBER(10,0))"""
  rows_to_insert = filter(lambda x: len(x)> 0, map(columns_to_type, data))
  cursor = db.cursor()
  cursor.execute("drop table us_who_flu_stats")
  cursor.execute(create_table)
  try:
    cursor.prepare("""INSERT INTO US_WHO_FLU_STATS (
          REGION, YEAR, WEEK, TOTAL_SPECIMENS,
          PERCENT_POSITIVE, A_H1, A_NO_SUBTYPE,
          A_H3, H1N1, A_TOTAL, B, H3N2v) VALUES 
          (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)""")
    cursor.executemany(None, rows_to_insert)
    db.commit()
  except Exception as e:
    print e


def main(filename):
  db = cx_Oracle.connect('fludb', 'flushot', 'localhost:1521/orcl')
  print "parsing datasets..."
  datasets = parseWHOFile(filename)
  print "writing to DB..."
  write_to_db(db, datasets)

if __name__ == "__main__":
  main(sys.argv[1])
