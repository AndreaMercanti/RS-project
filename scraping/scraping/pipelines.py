# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.exc import IntegrityError
from .db import DBManager

class ScrapingPipeline(object):
    def process_item(self, item, spider):
        dbMgr = DBManager.getInstance()
        
        try:
            dbMgr.addReview(item['user'], item['rating'], item['date'], item['review'], dbMgr.getFilmByID(item['filmID']))
        except IntegrityError:
            print('The review already exists')