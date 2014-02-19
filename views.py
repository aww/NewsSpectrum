
import os
from flask import Flask, render_template, request, jsonify, g
#import MySQLdb
import mysql.connector
import re
import urllib
from NewsSpectrum import app, examples
import dbinfo

#db = MySQLdb.connect(user="root", host="localhost", port=3306, db="world", passwd="root")

@app.before_request
def before_request():
    g.cnx = mysql.connector.connect(user=dbinfo.user,
                              password=dbinfo.password, 
                              database=dbinfo.database,
                              host=dbinfo.host,
                              port=dbinfo.port)

@app.teardown_request
def teardown_request(exception):
    cnx = getattr(g, 'cnx', None)
    if cnx is not None:
        cnx.close()


@app.route("/")
def search():
    url = request.args.get('url')
    if url:
        con = g.cnx.cursor()
        con.execute("SELECT url, topic_title FROM article WHERE url = %s", (url,))
        query_results = con.fetchall()
        if len(query_results) > 0:
            pass
        print examples
    return render_template('landing.html', examples=examples)


@app.route("/all_articles")
def list_all_articles():
    con = g.cnx.cursor()
    con.execute("SELECT grade_level, url, topic_title, reading_ease, ari FROM article ORDER BY topic_title, grade_level;")

    query_results = con.fetchall()
    #query_results = db.store_result().fetch_row(maxrows=0)
    all_articles = []
    for result in query_results:
        all_articles.append(dict(grade_level=result[0], url=result[1], topic_title=result[2], reading_ease=result[3], ari=result[4]))
    return render_template('all_articles.html', articles=all_articles)


@app.route("/articles")
def list_articles():
    json_url = "/_get_articles"
    quoted_url = request.args.get('url')
    if quoted_url:
        json_url += "?url=" + quoted_url
    else:
        quoted_url = "http%3A//www.techtimes.com/articles/2897/20140123/archaeologists-stumped-by-discovery-of-3600-year-old-pharaoh-woseribre-senebkay-tomb.htm"

    current_url = urllib.unquote(quoted_url)

    return render_template('articles.html', examples=map(lambda x: (urllib.quote(x[0]), x[1]), examples), json_url=json_url, current_url=current_url)


@app.route("/_get_articles")
def get_articles():
    con = g.cnx.cursor()

    topic = 'Bitcoin attacked by politicians and bankers at Davos'
    topic = "Don't panic, but the Milky Way Galaxy is forming 'inside out'"
    quoted_url = request.args.get('url')
    if quoted_url:
        current_url = urllib.unquote(quoted_url)
        con.execute('SELECT topic_title,url FROM article WHERE url = %s LIMIT 1', (current_url,))
        results = con.fetchall()
        if results:
            topic=results[0][0]
        else:
            return jsonify(articles=[])
    else:
        return jsonify(articles=[])

    con.execute("SELECT grade_level, url, title, body FROM article WHERE topic_title = %s AND LENGTH(body) > 200 ORDER BY grade_level DESC;", (topic,) )

    query_results = con.fetchall()

    n_groups = 14
    articles_per_group = len(query_results) / n_groups

    def group(lst, n):
        '''Group the list into tuples of size n except potentially the last group'''
        grps = zip(*[lst[i::n] for i in range(n)])
        if len(lst) % n != 0:
            grps.append( tuple(lst[-(len(lst) % n):]) )
        return grps

    selected_results = []
    current_grade_level = 0
    for group in group(query_results, articles_per_group):
        selected_result = group[0] # by default just pick the first one
        for result in group:
            if current_url == result[1]:
                selected_result = result
                current_grade_level = result[0]
        selected_results.append(selected_result)

    articles = []
    for result in selected_results:
        grade_level, url, title, body = result[:4]
        m_domain = re.match(r'http://(www\.)?([^/]*)', url)
        domain = "unknown"
        if m_domain:
            domain = m_domain.group(2)
        articles.append(dict(grade_level="%.1f" % grade_level, url=url, domain=domain, title=title, body=body))

    return jsonify(articles=articles, topic=topic, current_grade_level=current_grade_level, current_url=current_url)


@app.route("/topics")
def list_topics():
    con = g.cnx.cursor()
    con.execute("SELECT topic_title, url FROM article ORDER BY topic_title, grade_level;")

    prev_title = None
    query_results = con.fetchall()
    topics = []
    for result in query_results:
        title = result[0]
        url = result[1]
        if title == prev_title:
            topics[-1]['urls'].append(url)
        else:
            topics.append(dict(topic_title=title, urls=[url]))
            prev_title = title
    return render_template('topics.html', topics=topics) 

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
