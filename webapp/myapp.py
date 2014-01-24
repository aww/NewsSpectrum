
import os
from flask import Flask, render_template, request
#import MySQLdb
import mysql.connector
import re

app = Flask(__name__)
cnx = mysql.connector.connect(user='root', password='', 
                database='news', host='localhost')
#db = MySQLdb.connect(user="root", host="localhost", port=3306, db="world", passwd="root")

@app.route("/")
def search():
    url = request.args.get('q')
    if url:
        con.cnx.cursor()
        con.execute("SELECT url, topic_title FROM article WHERE url = %s", (url,))
        query_results = con.fetchall()
        if len(query_results) > 0:
            pass
    return render_template('landing.html')

# def hello():
#     return render_template('index.html') 

# @app.route("/db")
# def cities_page():
#     con = cnx.cursor()
#     con.execute("SELECT Name FROM City")
#     #db.query("SELECT Name FROM city;")

#     query_results = con.fetchall()
#     #query_results = db.store_result().fetch_row(maxrows=0)
#     cities = ""
#     for result in query_results:
#         cities += result[0] #unicode(result[0], 'utf8')
#         cities += "<br>"
#     return cities

# @app.route("/db_fancy")
# def cities_page_fancy():
#     con = cnx.cursor()
#     con.execute("SELECT Name, CountryCode, Population FROM City;")

#     query_results = con.fetchall()
#     #query_results = db.store_result().fetch_row(maxrows=0)
#     cities = []
#     for result in query_results:
#         cities.append(dict(name=result[0], country=result[1], population=result[2]))
#     return render_template('cities.html', cities=cities) 


@app.route("/all_articles")
def list_all_articles():
    con = cnx.cursor()
    con.execute("SELECT grade_level, url, topic_title, reading_ease, ari FROM article ORDER BY topic_title, grade_level;")

    query_results = con.fetchall()
    #query_results = db.store_result().fetch_row(maxrows=0)
    all_articles = []
    for result in query_results:
        all_articles.append(dict(grade_level=result[0], url=result[1], topic_title=result[2], reading_ease=result[3], ari=result[4]))
    return render_template('all_articles.html', articles=all_articles)


@app.route("/articles")
def list_articles():
    con = cnx.cursor()
    topic = "Don't panic, but the Milky Way Galaxy is forming 'inside out'"
    con.execute("SELECT grade_level, url, title, body FROM article WHERE topic_title = %s ORDER BY grade_level DESC;", (topic,) )

    query_results = con.fetchall()
    #query_results = db.store_result().fetch_row(maxrows=0)
    articles = []
    for i_article, result in enumerate(query_results):
        url = result[1]
        m_domain = re.match(r'http://(www\.)?([^/]*)', url)
        domain = "unknown"
        if m_domain:
            domain = m_domain.group(2)
        articles.append(dict(i=i_article, grade_level="%.1f" % result[0], url=url, domain=domain, title=result[2], body=result[3]))
    return render_template('articles.html', articles=articles, topic=topic) 



@app.route("/topics")
def list_topics():
    con = cnx.cursor()
    con.execute("SELECT topic_title FROM article GROUP BY topic_title;")

    query_results = con.fetchall()
    #query_results = db.store_result().fetch_row(maxrows=0)
    all_articles = []
    for result in query_results:
        all_articles.append(dict(topic_title=result[0]))
    return render_template('topics.html', articles=all_articles) 


@app.route('/<pagename>') 
def regularpage(pagename=None): 
    """ 
    Route not found by the other routes above. May point to a static template. 
    """ 
    return "You've arrived at " + pagename
    #if pagename==None: 
    #    raise Exception, 'page_not_found' 
    #return render_template(pagename) 

if __name__ == '__main__':
    print "Starting debugging server."
    app.run(debug=True, host='localhost', port=8000)


