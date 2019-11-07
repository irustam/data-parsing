# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaItemFollows(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = 'follows'
    user = scrapy.Field()
    follows = scrapy.Field()


class InstaItemPosts(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = 'posts'
    follow_id = scrapy.Field()
    posts = scrapy.Field()


class InstaItemComments(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = 'comments'
    post_shortcode = scrapy.Field()
    comments = scrapy.Field()


class InstaItemLikes(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = 'likes'
    post_shortcode = scrapy.Field()
    likes = scrapy.Field()