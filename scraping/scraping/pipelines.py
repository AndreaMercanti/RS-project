# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from .db import DBManager, Film

class ScrapingPipeline(object):
    def process_item(self, item, spider):
        db_mgr = DBManager.getInstance()
        film = Film(id=item['filmID'], title=item['filmTitle'])

        try:
            db_mgr.addFilm(item['filmID'], item['filmTitle'])
        except IntegrityError:
            print('The film already exists')
        
        try:
            db_mgr.addReview(item['user'], item['rating'], item['date'], item['review'], film)
        except IntegrityError:
            print('The review already exists')