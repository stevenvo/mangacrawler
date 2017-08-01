# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from mangacrawler.items import MangacrawlerItem
from scrapy.shell import inspect_response

class ThictruyentranhSpider(scrapy.Spider):
   name = "thichtruyentranh"
   allowed_domains = ["thichtruyentranh.com"]
   book_name = "NoName"
   REGEX_TAP_ID = re.compile(r".*? t.*?p (\d*)(.*$)")
   REGEX_IMG_URLS = re.compile(r"\'<img src=\"(.*?)\"")

   def __init__(self, *args, **kwargs):
      super(ThictruyentranhSpider, self).__init__(*args, **kwargs)
      self.book_name = kwargs.get('book_name')
      self.start_urls = [kwargs.get('url')]

   def parse(self, response):
    #   inspect_response(response, self)
      chap_urls = response.xpath('//ul[@class="ul_listchap"]/li/a/@href').extract()

      if chap_urls and len(chap_urls) > 0:
         for chap_url in chap_urls:
            chap_full_url = urlparse.urljoin(response.url, chap_url)
            yield scrapy.Request(chap_full_url, callback=self.parsePart)

   def parsePart(self, response):

      item = MangacrawlerItem()
      item['book_name'] = self.book_name
      page_title = response.xpath('//div[@class="item current"]/a/span/text()').extract()[0]
      m = self.REGEX_TAP_ID.search(page_title)
      part_id = m.group(1)
      chap_name = m.group(2)
      item['part_id'] = part_id
      item['chapter_name'] = chap_name
      item['image_urls'] = re.findall(self.REGEX_IMG_URLS, response.text)
      return item
