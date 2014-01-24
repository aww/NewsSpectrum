from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from gnews.items import GnewsItem
from BeautifulSoup import BeautifulSoup
from goose import Goose

limit_topics = 1000 #20
limit_articles_per_topic = 1000 #80

class ScienceSpider(Spider):
    name = "gnews_metaonly"
    allowed_domains = ["news.google.com"]
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
            article = self.g.extract(url=url)
            yield GnewsItem(gurl=response.url,
                            url=url,
                            title=article_link.xpath('a/span/text()').extract()[0],
                            topic_title=response.meta['topic'],
                            extract_title  = article.title,
                            extract_desc   = article.meta_description,
                            extract_text   = article.cleaned_text,
                            )
            #yield Request(url, callback=self.parse_article)
 
    # def parse_article(self, response):
    #     print "Article downloaded, contains", len(response.body), "characters."
    #     yield ArticleItem(url=response.url, body=response.body)
