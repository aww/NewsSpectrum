#/usr/bin/env python

import mysql.connector
#from mysql.connector import errorcode
import sys
import json
import nltk
from nltk_contrib.readability.readabilitytests import ReadabilityTool
#from readabilitytests import ReadabilityTool
#import nltk_contrib.readability.syllables_en

if len(sys.argv) != 2:
    print "build_database.py <data.json>"
    sys.exit(1)

class DbAccess(object):
    """Access database
    """
    def __init__(self, db_name, usr='root', pwd=''):
        self.db_name = db_name
        self.db_url = "localhost"
        self.connect(usr, pwd)
        self.cursor = self.cnx.cursor()

    def connect(self, usr, pwd=None):
        """Try to connect to DB
        """
        try:
            self.cnx = mysql.connector.connect(user=usr, password=pwd, 
                database=self.db_name, host=self.db_url)
        except mysql.connector.Error as err:
            if False: #err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif False: #err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)
            sys.exit(1)

    def close(self):
        """Disconnect from DB
        """
        self.cursor.close()
        self.cnx.close()

db = DbAccess('news')

db.cursor.execute('''
DROP TABLE IF EXISTS article;
''')

db.cursor.execute('''
CREATE TABLE article (
  url TEXT,
  title TEXT,
  topic_title TEXT,
  body TEXT,
  grade_level DOUBLE,
  reading_ease DOUBLE,
  ari DOUBLE
);
''')


with open(sys.argv[1], 'r') as f:
    for entry in json.load(f):
        text = entry['extract_text']
        if len(text) < 50:
            continue
        readability = ReadabilityTool(text)
        grade_level = readability.FleschKincaidGradeLevel() #getReportAll(text)
        reading_ease = readability.FleschReadingEase()
        ari = readability.ARI()
        print "%10.2f %10.2f %10.2f %s" % (grade_level, reading_ease, ari, entry['url'])
        db.cursor.execute("INSERT INTO `article` VALUES (%s, %s, %s, %s, %s, %s, %s);",
                          (entry['url'], entry['title'], entry['topic_title'], entry['extract_text'],
                           "%f" % grade_level, "%f" % reading_ease, "%f" % ari))


db.cnx.commit()

db.close()
