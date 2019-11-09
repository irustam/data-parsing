# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ZillowPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        mg_db = client.zillow_rustam
        self.collection = mg_db.zillow_fort_worth_tx

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item
