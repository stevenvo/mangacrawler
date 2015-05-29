# -*- coding: utf-8 -*-

# Scrapy settings for mangacrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mangacrawler'

SPIDER_MODULES = ['mangacrawler.spiders']
NEWSPIDER_MODULE = 'mangacrawler.spiders'

ITEM_PIPELINES = {'mangacrawler.pipelines.GocThuGianImagesPipeline':10}
IMAGES_STORE = "./downloaded-manga-jpegs"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mangacrawler (+http://www.yourdomain.com)'
