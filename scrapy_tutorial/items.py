# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    product_type = scrapy.Field()
    price_ex_tax = scrapy.Field()
    price_inc_tax = scrapy.Field()
    tax = scrapy.Field()
    avability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
