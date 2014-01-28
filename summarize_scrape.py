#/usr/bin/env python

import sys
import json
import nltk
from nltk_contrib.readability.readabilitytests import ReadabilityTool
#from readabilitytests import ReadabilityTool
#import nltk_contrib.readability.syllables_en
from collections import defaultdict
import re

if len(sys.argv) != 2:
    print "summarize_scrape.py <data.json>"
    sys.exit(1)

topics       = defaultdict(list)
domain_count = defaultdict(int)
ncl_count    = defaultdict(int)

with open(sys.argv[1], 'r') as f:
    for entry in json.load(f):
        topics[entry['topic_title']].append((entry['title'], entry['url']))
        # text = entry['extract_text']
        # if len(text) < 50:
        #     continue
        # readability = ReadabilityTool(text)
        # grade_level = readability.FleschKincaidGradeLevel() #getReportAll(text)
        # reading_ease = readability.FleschReadingEase()
        # ari = readability.ARI()
        # print "%10.2f %10.2f %10.2f %s" % (grade_level, reading_ease, ari, entry['url'])
        m_domain = re.match(r'http(s)?://(www\.)?([^/]+)', entry['url'])
        if m_domain:
            domain_count[m_domain.group(3)] += 1
        m_ncl = re.search(r'ncl=([^&]+)', entry['gurl'])
        if m_ncl:
            ncl_count[m_ncl.group(1)] += 1

for topic_title,titles in sorted(topics.items(), key=lambda x: len(x[1])):
    print "%5d" % len(titles), topic_title.encode('utf-8')
    for title, url in titles:
        print "   ", url
for ncl, count in sorted(ncl_count.items(), key=lambda x: x[1]):
    print "%5d %s" % (count, ncl)
print "Number of topics:", len(topics)
print "Number of NCLs  :", len(ncl_count)

for domain, count in sorted(domain_count.items(), key=lambda x: x[1]):
    print "%5d %s" % (count, domain)

