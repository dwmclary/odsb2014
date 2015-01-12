#! /usr/bin/env python

import feedparser
from bs4 import BeautifulSoup
import json
import time

urls = {"top_news":"http://feeds.reuters.com/reuters/topNews", \
            "health": "http://feeds.reuters.com/reuters/healthNews", \
            "healthcare":"http://feeds.reuters.com/reuters/UShealthcareNews", \
            "science":"http://feeds.reuters.com/reuters/scienceNews"}

etags = {"top_news": None, "health": None, "healthcare": None, "science": None}

done = False

while not done:
    for k, v in urls.items():
        if etags[k]:
            d = feedparser.parse(v, etag=etags[k])
        else:
            d = feedparser.parse(v)
            for e in d.entries:
                doc = json.dumps({"category":k, "title":e.title.strip(), "summary":BeautifulSoup(e.summary).text.strip()})
                print doc
        etags[k] = d.etag
        time.sleep(60)
