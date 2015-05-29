# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from mangacrawler.items import MangacrawlerItem


class GocthugianSpider(scrapy.Spider):
   name = "gocthugian"
   allowed_domains = ["gocthugian.com.vn"]
   book_name = "NoName"

   def __init__(self, *args, **kwargs): 
      super(GocthugianSpider, self).__init__(*args, **kwargs) 
      self.book_name = kwargs.get('book_name')
      self.start_part_id = int(kwargs.get('start'))
      self.stop_part_id = int(kwargs.get('stop'))
      self.start_urls = [kwargs.get('start_url')]

   def parse(self, response):
      parts = response.xpath('//div[@class="VIOI"]/a') #Tập 
      for part in parts:
         part_id = int(part.xpath('./text()').re('T.*?p (\d*)')[0])
         if part_id >= self.start_part_id and part_id <= self.stop_part_id:
            part_link = urlparse.urljoin(response.url, part.xpath('./@href').extract()[0])
            yield scrapy.Request(part_link, callback=self.parsePart)

   def parsePart(self, response):
      chapters = scrapy.Selector(response).xpath('//li[@class="ChI"]/a')
      for chapter in chapters:
         chapter_link = urlparse.urljoin(response.url, chapter.xpath('./@href').extract()[0])
         yield scrapy.Request(chapter_link, callback=self.parseChapterPage)

   def parseChapterPage(self, response):
      item = MangacrawlerItem()
      item['book_name'] = self.book_name
      page_title = response.xpath('//div[@class="FPH"]/h1/text()').extract()[0]
      (item['part_id'], item['chapter_id']) = re.findall("T.*?p (\d*) - Chapter (\d*)", page_title)[0]
      item['image_urls'] = response.xpath('//div[@class="TTCD"]/img/@src').extract()
      return item