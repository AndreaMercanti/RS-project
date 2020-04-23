# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapingItem
from datetime import datetime

class FetcherSpider(scrapy.Spider):
    name = 'fetcher'
    allowed_domains = ['imdb.com']

    def __init__(self, **kwargs):
        if not hasattr(self, 'ajax_url'):
            self.ajax_url = None # instance variable
        super().__init__(**kwargs)

    def start_requests(self):
        self.ajax_url = 'https://www.imdb.com/title/tt0113497/reviews/_ajax?sort=userRating&dir=desc&ratingFilter=0'
        yield scrapy.Request(self.ajax_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = ScrapingItem()
        reviews = response.css('.collapsable')
        
        for review in reviews:
            user = review.css(".display-name-link a::text").get()
            rating = review.css(".rating-other-user-rating span::text").extract()
            date = review.css(".review-date::text").get()
            review = review.css(".show-more__control::text").extract()

            date = str(datetime.strptime(date, '%d %B %Y').date()) # parse the date and format it in a 'YYYY-MM-DD'-like string

            item['user'] = user
            item['rating'] = rating
            item['date'] = date
            item['review'] = review
            
            yield item
        
        next_page = response.css(".load-more-data").xpath('@data-key').get()
        if next_page is not None:
            yield scrapy.Request(self.ajax_url + '&ref_=undefined&paginationKey=' + next_page, callback=self.parse)
