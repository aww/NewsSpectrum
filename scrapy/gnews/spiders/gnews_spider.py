from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from gnews.items import GnewsItem
from BeautifulSoup import BeautifulSoup
from goose import Goose

limit_topics = 100
limit_articles_per_topic = 1000

class ScienceSpider(Spider):
    name = "gnews"
    allowed_domains = []
    start_urls = [
        "https://news.google.com/news/section?pz=1&cf=all&topic=snc", # science
        "https://news.google.com/news/section?pz=1&cf=all&topic=tc", # technology
        "https://news.google.com/news/section?pz=1&cf=all&topic=m",  # health
        "https://news.google.com/news/section?pz=1&cf=all&topic=b",  # business
        ]

    g = Goose()

    def parse(self, response):
        sel = Selector(response)
        selected_esc_body = sel.xpath('//div[@class="esc-body"]')
        print "Found", len(selected_esc_body), "topics"
        for i, esc in enumerate(selected_esc_body):
            if i >= limit_topics:
                break
            topic_title = esc.xpath('div/table/tbody/tr/td/div/h2/a/span/text()').extract()
            url = esc.xpath('div/table/tbody/tr/td/div/div[@class="moreLinks"]/a/@href').extract()
            if topic_title and url:
                req = Request('https://news.google.com' + url[0], callback=self.parse_fullcoverage)
                req.meta['topic'] = topic_title[0]
                yield req
            else:
                if not topic_title:
                    if not topic_title:
                        print "No title text or details URL found in"
                    else:
                        print "No title text found in"
                else:
                        print "No details URL found in"
                #print "  ===="
                #print BeautifulSoup(esc.extract()).prettify()
                #print "  ===="

    def parse_fullcoverage(self, response):
        sel = Selector(response)
        for i, article_link in enumerate(sel.xpath('//h2[@class="title"]')):
            if i >= limit_articles_per_topic:
                break
            url = article_link.xpath('a/@href').extract()[0]
            req = Request(url, callback=self.parse_article)
            req.meta['gurl']        = response.url
            req.meta['title']       = article_link.xpath('a/span/text()').extract()[0]
            req.meta['topic_title'] = response.meta['topic']
            yield req
        for path in sel.xpath('//div[@id="pagination"]/table/tr/td/a/@href').extract():
            req = Request('https://news.google.com' + path, callback=self.parse_fullcoverage)
            req.meta['topic'] = response.meta['topic']
            yield req
 
    def parse_article(self, response):
        print "Article contains %6d characters: %s" % (len(response.body), response.url)
        article = self.g.extract(raw_html=response.body)
        return GnewsItem(gurl          = response.meta['gurl'],
                         url           = response.url,
                         title         = response.meta['title'],
                         topic_title   = response.meta['topic_title'],
                         extract_title = article.title,
                         extract_desc  = article.meta_description,
                         extract_text  = article.cleaned_text,
                         )
