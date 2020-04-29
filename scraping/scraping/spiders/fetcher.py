# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapingItem
from datetime import datetime
import json

class FetcherSpider(scrapy.Spider):
    name = 'fetcher'
    allowed_domains = ['imdb.com']

    def __init__(self, **kwargs):
        if not hasattr(self, 'ajax_url'):
            self.ajax_url = None # instance variable
        if not hasattr(self, 'film_id'):
            self.film_id = None # instance variable
        if not hasattr(self, 'film_title'):
            self.film_title = None # instance variable
        super().__init__(**kwargs)

    def start_requests(self):
        with open('movie_dataset.json', 'r') as file:
            movie = json.loads(file.readline())
            self.film_id = movie['imdbID']
            self.film_title = movie['Title']
            self.ajax_url = 'https://www.imdb.com/title/{}/reviews/_ajax?sort=userRating&dir=desc&ratingFilter=0'.format(self.film_id)
            yield scrapy.Request(self.ajax_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = ScrapingItem()
        reviews = response.css('.collapsable')
        
        for review in reviews:
            user = review.css(".display-name-link a::text").get()
            rating_components = review.css(".rating-other-user-rating span::text").extract()
            date = review.css(".review-date::text").get()
            review_components = review.css(".show-more__control::text").extract()

            # PARSING AND BETTER FORMATTING THE DIFFERENT ELEMS
            date = datetime.strptime(date, '%d %B %Y').date() # formatting in a 'YYYY-MM-DD'-like string
            review_str = ''.join(review_components[0:-2]) # compatting all the review components into one string, but the last two
            rating = ''.join(rating_components) # compatting all rating components into one string

            item['filmID'] = self.film_id
            item['filmTitle'] = self.film_title
            item['user'] = user
            item['rating'] = rating
            item['date'] = date
            item['review'] = review_str
            
            yield item
        
        next_page = response.css(".load-more-data").xpath('@data-key').get()
        if next_page is not None:
            yield scrapy.Request(self.ajax_url + '&ref_=undefined&paginationKey=' + next_page, callback=self.parse)
