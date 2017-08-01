# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MangacrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    part_id = scrapy.Field()
    chapter_id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    chapter_name = scrapy.Field()
    # source = scrapy.Field()
    # image_counter = scrapy.Field()
    pass
