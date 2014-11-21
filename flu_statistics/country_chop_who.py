#! /usr/bin/env python
""" Working version of a parser/db-writer for WHO Continent-Level data.  Will be reformatted as an iPython Notebook as well."""

import sys
import cx_Oracle
import pprint
import re
import string

def write_to_db(db, dataset):
  dt = "DROP TABLE %s" % dataset['title']
  cursor = db.cursor()
  try:
    cursor.execute(dt)
  except:
    pass
  ctine = """CREATE TABLE %s (
	  region VARCHAR(12),
	  country VARCHAR(500),
	  year NUMBER,
	  week NUMBER,
	  measure NUMBER,
          CONSTRAINT %s_id PRIMARY KEY (country, year, week)
          )""" % (dataset['title'], dataset['title'])
  try:
    cursor.execute(ctine)
  except Exception as e:
    print e
    print "failed to create table", dataset['title']
    pass
  for country in dataset['data']:
    try:
      cursor.prepare("INSERT INTO %s (region, country, year, week, measure) VALUES (:1, :2, :3, :4, :5)" % dataset['title'])
      cursor.executemany(None, country)
      db.commit()
    except Exception as e:
      print e
      print country[0]


def make_tablename(d):
  title_string = d.split("|")[0]
  if "specimen" in title_string:
    title = title_string.split("->")[-1].strip()+"_Specimens"
    if "processed" in title_string:
      title += "_proc"
    else:
      title += "_recv"
  else:
    title = title_string.split("->")[-1].strip()+"_Infections"
  title = re.sub("\(", "", title)
  title = re.sub("\)", "", title)
  title = re.sub(" ","_", title)
  return title[:25]

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
      t.append((region_code, r[0], int(dates[i-1][0]), int(dates[i-1][1]), int(re.sub(",","",r[i]))))
    return t
  data = map(lambda x: row_to_tuple(dates, x), data)
  return data

def parseWHOCountryFile(filename):
  region = re.sub("WHO+", "",filename)
  region = re.sub(".psv", "", region)
  region = re.sub("\+","", region)
  region = region.split("/")[-1]
  raw = open(filename).readlines()
  big_splits = []
  for i in range(len(raw)):
    if len(raw[i].split("|")) == 2:
      big_splits.append(i)
  datasets = []
  #pp = pprint.PrettyPrinter(indent=4)
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
    #pp.pprint(ds)
  return datasets

def build_view(datasets):
  view = """CREATE OR REPLACE VIEW flu_statistics AS
  SELECT a.region, a.country, a.year, a.week, \n"""
  from_clause = " from \n"
  where_clause = " where \n"
  column_creation = ""
  table_creation = ""
  join_creation = ""
  for i in range(len(datasets)):
    column_creation += "{0}.measure as {1}".format(string.ascii_lowercase[i], datasets[i]['title'])
    
    table_creation += "{0} {1}".format(datasets[i]['title'], string.ascii_lowercase[i])
    
    if (i < len(datasets)-1):
      column_creation += ",\n"
      table_creation += ",\n"
      join_creation += "{1}.country = {0}.country and {1}.year = {0}.year and {1}.week = {0}.week \n".format(string.ascii_lowercase[i], string.ascii_lowercase[i+1])
      if (i < len(datasets)-2):
        join_creation += "and\n"
    else:
      column_creation += "\n"
      table_creation += "\n"
     

  view += column_creation + from_clause + table_creation + where_clause + join_creation
  return view
    
def main(filename):
  db = cx_Oracle.connect('fludb', 'flushot', 'localhost:1521/orcl')
  print "parsing datasets..."
  datasets = parseWHOCountryFile(filename)
  print "writing to DB..."
  for dataset in datasets:
    write_to_db(db, dataset)
  print "creating view..."
  c = db.cursor()
  c.execute(build_view(datasets))

if __name__ == "__main__":
  main(sys.argv[1])
  


