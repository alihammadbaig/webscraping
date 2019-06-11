#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy


class JobinfoSpider(scrapy.Spider):

    name = 'jobdetails'
    allowed_domains = ['joboutlook.gov.au']
    start_urls = ['https://joboutlook.gov.au/Industry.aspx']

    def parse(self, response):

        industry_details_page_urls = \
            response.css('article > div.career-title > h2 > a::attr(href)'
                         ).extract()

        # url = response.urljoin(industry_details_page_urls[0])
        # yield scrapy.Request(url=url, callback=self.parse_industry_profiles)

        # Industry details page

        for url in industry_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url,
                                 callback=self.parse_industry_profiles)

    def parse_industry_profiles(self, response):
        profile_details_page_urls = \
            response.css('article > div.career-title > h3 > a::attr(href)'
                         ).extract()

        # Job profile details page

        for url in profile_details_page_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_profile_details)

    def parse_profile_details(self, response):
        fast_facts = \
            response.css('ul.snapshot > li > span.snapshot-data::text')

        yield {
            'industry': response.css('div.breadcrumb-col > ul > li:nth-of-type(3) > a::text').extract_first().strip(),
            'job_profile': response.css('div.page-title-col > h1::text').extract_first().strip(),
            'anzsco_code': response.css('div.anzsco > abbr::text').extract_first().replace('ANZSCO ID ', '').strip(),
            'avg_weekly_pay': fast_facts[0].extract().strip(),
            'future_growth': fast_facts[1].extract().strip(),
            'skill_level': fast_facts[2].extract().strip(),
            'employment_size': fast_facts[3].extract().strip(),
            'unemployment': fast_facts[4].extract().strip(),
            'male_share': fast_facts[5].extract().strip(),
            'female_share': fast_facts[6].extract().strip(),
            'full_time': fast_facts[7].extract().strip(),
        }
