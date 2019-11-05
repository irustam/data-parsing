# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class InstaPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.mg_db = client.insta_rustam

    def process_item(self, item, spider):
        if item.get('user'):
            collection = self.mg_db.insta_user_follows
            collection.insert_one(item)
        elif item.get('follow_id'):
            collection = self.mg_db.insta_posts
            collection.insert_one(item)
        elif item.get('comments'):
            collection = self.mg_db.insta_post_comments
            collection.insert_one(item)
        elif item.get('likes'):
            collection = self.mg_db.insta_post_likes
            collection.insert_one(item)
        return item
