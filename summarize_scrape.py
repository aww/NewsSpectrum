#/usr/bin/env python

import sys
import json
import nltk
from nltk_contrib.readability.readabilitytests import ReadabilityTool
#from readabilitytests import ReadabilityTool
#import nltk_contrib.readability.syllables_en

if len(sys.argv) != 2:
    print "summarize_scrape.py <data.json>"
    sys.exit(1)

from collections import defaultdict
topics = defaultdict(list)
with open(sys.argv[1], 'r') as f:
    for entry in json.load(f):
        topics[entry['topic_title']].append(entry['title'])
        # text = entry['extract_text']
        # if len(text) < 50:
        #     continue
        # readability = ReadabilityTool(text)
        # grade_level = readability.FleschKincaidGradeLevel() #getReportAll(text)
        # reading_ease = readability.FleschReadingEase()
        # ari = readability.ARI()
        # print "%10.2f %10.2f %10.2f %s" % (grade_level, reading_ease, ari, entry['url'])

for topic_title,titles in topics.items():
    print "%5d %s" % (len(titles), topic_title)
