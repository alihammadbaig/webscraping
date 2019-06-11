#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from joboutlook.items import JoboutlookItem


class JobinfoSpider(scrapy.Spider):

    name = 'jobinfo'
    allowed_domains = ['joboutlook.gov.au']
    start_urls = ['https://joboutlook.gov.au/Industry.aspx']

    def parse(self, response):
        urls = response.css(
            'article > div.career-title > h2 > a::attr(href)').extract()
        item = JoboutlookItem()
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
        item['profile_page_url'] = response.url

        profile_details_page_urls = response.css(
            'article > div.career-title > h3 > a::attr(href)').extract()

        for url in profile_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_profile_details, meta={'item': item})

    def parse_profile_details(self, response):
        item = response.meta['item']
        item['profile_detail_page_url'] = response.url

        fast_facts = response.css(
            'ul.snapshot > li > span.snapshot-data::text')

        item['industry'] = response.css(
            'div.breadcrumb-col > ul > li:nth-of-type(3) > a::text').extract_first().strip(),
        item['anzsco_code'] = response.css(
            'div.anzsco > abbr::text').extract_first().replace('ANZSCO ID ', '').strip()
        item['job_profile'] = response.css(
            'div.page-title-col > h1::text').extract_first().strip()
        item['avg_weekly_pay'] = fast_facts[0].extract().strip()
        item['future_growth'] = fast_facts[1].extract().strip()
        item['skill_level'] = fast_facts[2].extract().strip()
        item['employment_size'] = fast_facts[3].extract().strip()
        item['unemployment'] = fast_facts[4].extract().strip()
        item['male_share'] = fast_facts[5].extract().strip()
        item['female_share'] = fast_facts[6].extract().strip()
        item['full_time'] = fast_facts[7].extract().strip()

        yield item
