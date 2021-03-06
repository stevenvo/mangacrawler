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
import logging


class GocThuGianImagesPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        # print "get_media_requests"

        # return [Request(x, meta={'chapter_id': item["chapter_id"], 'part_id': item["part_id"], 'book_name': item["book_name"]})
        #       for x in item.get('image_urls', [])]

        for key, image_url in enumerate(item['image_urls']):
            yield Request(image_url,
                          meta={'chapter_id': item.get('chapter_id', ''),
                                'chapter_name': item.get('chapter_name', ''),
                                'part_id': item.get('part_id', ''),
                                'book_name': item.get('book_name', ''),
                                'image_key': key})

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        # print "get_images"
        for key, image, buf, in super(GocThuGianImagesPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
                yield key, image, buf

    def change_filename(self, key, response):
        # Comment this code as sometimes website uses the same filename (different path)
        # for all images in the chapter
        # org_filename = response.url.split('/')[-1]
        # if re.findall('(\d*).jpg', org_filename)[0] != '':
        #    image_id = int(re.findall('(\d*).jpg', org_filename)[0])
        # else:
        #    image_id = int(re.findall('Trang(\d*)_TSMini.jpg', org_filename)[0])

        # Use image key (generated in get_media_request by image crawling sequence) instead
        image_id = response.meta['image_key']

        if response.meta['chapter_id']:
            new_filename = '{0}-Tap{1}-Chapter{2:03}-Image{3:06}.jpg'.format(response.meta['book_name'], response.meta['part_id'], int(response.meta['chapter_id']), image_id)
        else:
            if response.meta['chapter_name']:
                new_filename = '{0}-Tap{1}{2}-Image{3:06}.jpg'.format(response.meta['book_name'], response.meta['part_id'], response.meta['chapter_name'].encode('utf-8'), image_id)
            else:
                new_filename = '{0}-Tap{1}-Image{2:06}.jpg'.format(response.meta['book_name'], response.meta['part_id'], image_id)
        return '%s' % (new_filename)


class MangacrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
