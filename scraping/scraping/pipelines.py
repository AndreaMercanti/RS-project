# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from .db import DBManager, Film

class ScrapingPipeline(object):
    film = None

    def process_item(self, item, spider):
        dbMgr = DBManager.getInstance()
        
        if self.film is None or self.film.id != item['filmID']:
            self.film = dbMgr.getFilmByID(item['filmID'])
            # self.film = Film(id=item['filmID'], title=item['filmTitle'])
            # dbMgr.addFilm(item['filmID'], item['filmTitle'])
        
        repr(self.film)

        # try:
        #     dbMgr.addFilm(item['filmID'], item['filmTitle'])
        # except IntegrityError:
        #     print('The film already exists')
        
        try:
            dbMgr.addReview(item['user'], item['rating'], item['date'], item['review'], self.film)
        except IntegrityError:
            print('The review already exists')