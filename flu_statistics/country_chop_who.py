#! /usr/bin/env python
""" Working version of a parser/db-writer for WHO Continent-Level data.  Will be reformatted as an iPython Notebook as well."""

import sys
import cx_Oracle
import pprint
import re

def write_to_db(db, dataset):
  ctine = """CREATE TABLE IF NOT EXISTS %s (
	  region VARCHAR(12),
	  country VARCHAR(300) PRIMARY KEY,
	  year NUMBER
	  week NUMBER
	  value NUMBER)""" % dataset['title']
  cursor = db.cursor()
  cursor.execute(ctine)
  cursor.prepare("INSERT INTO %s (region, country, year, week, value) VALUES (:1, :2, :3, :4, :5)" % dataset['title'])
  cursor.executemany(None, dataset['data'])
  db.commit()


def make_tablename(d):
  title_string = d.split("|")[0]
  if "specimen" in title_string:
    title = title_string.split("->")[-1].strip()+"Specimens"
  else:
    title = title_string.split("->")[-1].strip()+"Infections"
  return title

def makerows(region_code, data):
  dateprefix = data[0]
  dates = map(lambda x: x.split(), dateprefix.strip().split("|")[1:])
  dates = map(lambda x: [x[0], x[-1]], dates)
  data = map(lambda x: x.strip().split("|"), data[1:])
  # what we're really doing here is pivoting the data so that we can have country, year, week, value
  # for each row of raw data, we want a list of tuple (country, year, week, value)
  def row_to_tuple(dates, r):
    t = []
    for i in range(1,len(r)):
      t.append((region_code, r[0], dates[i-1][0], dates[i-1][1], r[i]))
    return t
  data = map(lambda x: row_to_tuple(dates, x), data)
  return data

def parseWHOCountryFile(filename):
  region = re.sub("WHO+", "",filename)
  region = re.sub(".psv", "", region)
  region = re.sub("\+","", region)
  raw = open(filename).readlines()
  big_splits = []
  for i in range(len(raw)):
    if len(raw[i].split("|")) == 2:
      big_splits.append(i)
  datasets = []
  pp = pprint.PrettyPrinter(indent=4)
  for i in range(0,len(big_splits),2):
    ds = {}
    ds['title'] = raw[big_splits[i]]
    ds['title'] = make_tablename(ds['title'])
    ds['period'] = raw[big_splits[i+1]]
    if i < len(big_splits)-2:
      ds['starts'] = big_splits[i+1]+1
      ds['ends'] = big_splits[i+2]-1
    else:
      ds['starts'] = big_splits[i+1]+1
      ds['ends'] = len(raw)-1
    ds['data'] = raw[ds['starts']:ds['ends']]
    ds['data'] = makerows(region, ds['data'])
    datasets.append(ds)
    pp.pprint(ds)
  for ds in datasets:
    print ds['title']
  return datasets
    
def main(filename):
  db = cx_Oracle.connect('fludb', 'flushot', 'localhost:1521/orcl')
  datasets = parseWHOCountryFile(filename)
  for dataset in datasets:
    write_to_db(db, dataset)
  

if __name__ == "__main__":
  main(sys.argv[1])
  


