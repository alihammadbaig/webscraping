# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        urls = response.css('div.quote > span > a::attr(href)').extract()

        # Author details
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            print("Next URL: " + next_page_url)
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = next_page_url, callback = self.parse)

    def parse_details(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first()
            , 'birth_date': response.css('span.author-born-date::text').extract_first()
        }

    def parse_details(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'birth_date': response.css('span.author-born-date::text').extract_first(),
        }
    # # this parser is for one URL only
    # def parse_old(self, response):
    #     self.log('URL: ' + response.url)

    #     quote = response.css('div.quote')
    #     print(quote.css('small.author::text').extract_first())

    #     for quote in response.css('div.quote'):
    #         self.log(quote)
    #         item = {
    #             'author-name': quote.css('small.author::text').extract_first(),
    #             'text': quote.css('span.text::text').extract_first(),
    #             'tags': quote.css('a.tag::text').extract()
    #         }
    #         yield item
