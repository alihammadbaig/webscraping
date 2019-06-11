# -*- coding = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in = scrapy.Field()
# https = scrapy.Field()

import scrapy
from scrapy.item import Item, Field


class JoboutlookItem(scrapy.Item):
    main_page_url = Field()
    profile_page_url = Field()
    profile_detail_page_url = Field()
    industry = Field()
    job_profile = Field()
    anzsco_code = Field()
    avg_weekly_pay = Field()
    future_growth = Field()
    skill_level = Field()
    employment_size = Field()
    unemployment = Field()
    male_share = Field()
    female_share = Field()
    full_time = Field()
