# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from config import mongo_url, db_name, collections


class InstaPipeline(object):
    def __init__(self):
        client = MongoClient(mongo_url)
        self.mg_db = client[db_name]

    def process_item(self, item, spider):
        collection = self.mg_db[collections[item._class.name]]
        collection.insert_one(item)
        return item
