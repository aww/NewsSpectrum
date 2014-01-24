# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GnewsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url            = Field()
    gurl           = Field()
    title          = Field()
    topic_title    = Field()
    extract_title  = Field()
    extract_desc   = Field()
    extract_text   = Field()
    extract_imgsrc = Field()
