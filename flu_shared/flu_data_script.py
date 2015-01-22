
import json
import urllib2

url = "http://flu-vaccination-map.hhs.gov/api/v1/states.json"

data = json.load(urllib2.urlopen(url))

outfile = open('flu_data.txt', 'w')

for record in data['results']:
	print >> outfile, json.dumps(record)

outfile.close()

lines = open("flu_data.txt").readlines()
line_size=map(lambda x: len(x), lines)