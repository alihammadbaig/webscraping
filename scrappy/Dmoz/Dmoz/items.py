# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    main_page_url = scrapy.Field()
    profile_page_url = scrapy.Field()
    profile_detail_page_url = scrapy.Field()
    anzsco_code = scrapy.Field()
    avg_weekly_pay = scrapy.Field()
