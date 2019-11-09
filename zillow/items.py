# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import TakeFirst

def cleaner_address(item: list):
    len_item = int(len(item)/2)
    item = item[:len_item]
    item.reverse()
    result = item.pop()
    for i in item[:]:
        result += i
    return result


def cleaner_description(item: list):
    item.reverse()
    result = item.pop()
    for i in item[:]:
        result += i
    return result


def cleaner_facts(item):
    result = {}
    i = 0
    while i < len(item):
        result.update({item[i]: item[i+1]})
        i += 2
    return result


def cleaner_facts_more(item):
    item = item[0]
    result = {}
    for b_header, block in item.items():
        if len(block):
            block_dict = {}
            for sb_header, sub_block in block.items():
                if len(sub_block):
                    facts_dict = {}
                    for fact in sub_block:
                        f_lst = fact.replace('\n', ' ').split(': ')
                        facts_dict.update({f_lst[0]: f_lst[1]})

                    block_dict.update({sb_header: facts_dict})
            result.update({b_header: block_dict})
    return result


class ZillowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=cleaner_address)
    price = scrapy.Field(output_processor=TakeFirst())
    zestimate_price = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=cleaner_description)
    facts_and_features = scrapy.Field(output_processor=cleaner_facts)
    facts_and_features_more = scrapy.Field(output_processor=cleaner_facts_more)
    images = scrapy.Field()
