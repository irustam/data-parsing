# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import json

def cleaner_dict_data(items):
    result = items[1].split(' || {};')[0]\
                            .replace('<script type="text/javascript">window.__initialData__ = ', '')\
                            .replace('\\u002F', '/')
    result = json.loads(result)['item']['item']

    drop_keys = ['refs',
                'sharing',
                'geoReferences',
                'titleGenerated',
                'stats',
                'contacts',
                'autodeal',
                'autoteka',
                'needToCheckCreditInfo',
                'autotekaTeaser',
                'adjustParams',
                'needToCheckSimilarItems'
                'seller'
                 ]
    for itm in drop_keys:
        try:
            result.pop(itm)
        except:
            pass

    return result

def cleaner_photo(values):
    print(11)
    return values['640x480']

def cleaner_params(item):
    result = item.split('">')[-1].split(': </span>')
    key = result[0]
    value = result[1][:-5].replace(u'\xa0', ' ').rstrip()
    return {key: value}

def cleaner_props(items):
    print(21)
    if items[0]['success']:
        return items[0]['spec']
    return None

def cleaner_vin(items):
    print(31)
    return items[0]['result']

class AvitoAutoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    data = scrapy.Field(output_processor=TakeFirst())
    properties = scrapy.Field(output_processor=cleaner_props)
    vin_data = scrapy.Field(output_processor=cleaner_vin)
    images = scrapy.Field(input_processor=MapCompose(cleaner_photo))