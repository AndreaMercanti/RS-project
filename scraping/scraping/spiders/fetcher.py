# -*- coding: utf-8 -*-
import scrapy


class FetcherSpider(scrapy.Spider):
    name = 'fetcher'
    allowed_domains = ['imdb.com']
    start_urls = ['http://imdb.com/']

    def parse(self, response):
        pass
