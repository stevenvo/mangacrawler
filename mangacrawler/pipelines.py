# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from PIL import Image
from cStringIO import StringIO
import re

class GocThuGianImagesPipeline(ImagesPipeline):

  CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')

  # name information coming from the spider, in each item
  # add this information to Requests() for individual images downloads
  # through "meta" dict
  def get_media_requests(self, item, info):
    print "get_media_requests"
    return [Request(x, meta={'chapter_id': item["chapter_id"], 'part_id': item["part_id"], 'book_name': item["book_name"]})
      for x in item.get('image_urls', [])]

  # this is where the image is extracted from the HTTP response
  def get_images(self, response, request, info):
    print "get_images"
    for key, image, buf, in super(GocThuGianImagesPipeline, self).get_images(response, request, info):
      if self.CONVERTED_ORIGINAL.match(key):
        key = self.change_filename(key, response)
      yield key, image, buf

  def change_filename(self, key, response):
    org_filename = response.url.split('/')[-1]
    new_filename = '{0}-Tap{1}-Chapter{2}-Image{3}'.format(response.meta['book_name'], response.meta['part_id'], response.meta['chapter_id'], org_filename)
    return '%s' % (new_filename)
    # return "full/%s.jpg" % response.meta['chapter'][0]


class MangacrawlerPipeline(object):
  def process_item(self, item, spider):
    return item