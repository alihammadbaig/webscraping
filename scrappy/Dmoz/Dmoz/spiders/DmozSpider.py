# -*- coding: utf-8 -*-
import scrapy
from Dmoz.items import DmozItem


class DmozspiderSpider(scrapy.Spider):
    name = 'DmozSpider'
    allowed_domains = ['joboutlook.gov.au']
    start_urls = ['https://joboutlook.gov.au/Industry.aspx']

    def parse(self, response):
        urls = response.css(
            'article > div.career-title > h2 > a::attr(href)').extract()
        item = DmozItem()
        item['main_page_url'] = response.url

        for url in urls:
            url = response.urljoin(url)
            request = scrapy.Request(url=url,
                                     callback=self.parse_industry_profiles)
            request.meta['item'] = item
            yield request

    def parse_industry_profiles(self, response):
        self.log('__fun parse_industry_profiles__')
        item = response.meta['item']
        # item['profile_page_url'] = response.url
        # yield item
        profile_details_page_urls = response.css(
            'article > div.career-title > h3 > a::attr(href)').extract()

        for url in profile_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_profile_details, meta={'item': item})

    def parse_profile_details(self, response):
        self.log('__fun parse_profile_details__')
        item = response.meta['item']
        fast_facts = response.css(
            'ul.snapshot > li > span.snapshot-data::text')
        item['anzsco_code'] = response.css(
            'div.anzsco > abbr::text').extract_first().replace('ANZSCO ID ', '').strip()
        item['avg_weekly_pay'] = fast_facts[0].extract().strip()
        yield item
