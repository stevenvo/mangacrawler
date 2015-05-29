# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from mangacrawler.items import MangacrawlerItem


class GocthugianSpider(scrapy.Spider):
  name = "gocthugian"
  allowed_domains = ["gocthugian.com.vn"]
  start_urls = (
  'http://gocthugian.com.vn/truyen/v2201/', #tap 9
  'http://gocthugian.com.vn/truyen/v2202/',
  'http://gocthugian.com.vn/truyen/v2203/',
  'http://gocthugian.com.vn/truyen/v2204/', #tap 12
  )

  def parse(self, response):
    chapters = scrapy.Selector(response).xpath('//li[@class="ChI"]/a')
    for chapter in chapters:
      chapter_name = chapter.xpath('text()').re('(Chapter \d*)')[0]
      chapter_link = urlparse.urljoin(response.url, chapter.xpath('./@href').extract()[0])
      yield scrapy.Request(chapter_link, callback=self.parseChapterPage)

  def parseChapterPage(self, response):
    item = MangacrawlerItem()
    item['chapter'] = response.xpath('//div[@id="SiteMapPath"]').re('(Chapter \d*)')[0]
    item['image_urls'] = response.xpath('//div[@class="TTCD"]/img/@src').extract()
    return item