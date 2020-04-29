# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from db import engine, Film, Review

class ScrapingPipeline(object):
    def process_item(self, item, spider):
        Session = sessionmaker(bind=engine)
        session = Session()
        
        film = Film(id=item['film_id'], title=item['film_title'])
        session.add(film)

        review = Review(user=item['user'], rating=item['rating'], date=item['date'], review=item['review'], film=film)
        session.add(review)

        session.commit()
        session.close()