
import json
import urllib2

url = "http://flu-vaccination-map.hhs.gov/api/v1/states.json"

data = json.load(urllib2.urlopen(url))

with open('flu_data.txt', 'w') as outfile:
	json.dump(data, outfile)

