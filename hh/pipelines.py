# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class HhPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        mg_db = client.hh_rustam
        self.collection_vacancies = mg_db.hh_vacancies
        self.collection_companies = mg_db.hh_companies

    def process_item(self, item, spider):
        if item.get('company_name'):
            self.collection_companies.update({'company_hh_page': item['company_hh_page']}, {'$set': item}, upsert=True)
        elif item.get('company_url'):
            self.collection_companies.update({'company_hh_page': item['company_hh_page']}, {'$set': {'company_url': item['company_url']}}, upsert=False)
        elif item.get('title'):
            self.collection_vacancies.insert_one(item)
        return item
