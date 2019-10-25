# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqldb.batabase import FlatsBase
from sqldb.models import Flats, Images, Addresses, Sellers, Base

class AvitoFlatsPipeline(object):
    def __init__(self):
        db_url = 'sqlite:///av_flats_base.sqlite'
        self.db = FlatsBase(Base, db_url)

    def process_item(self, item, spider):
        #print(1)
        seller = self.db.session.query(Sellers).filter_by(seller_url=item.get('seller_url')).first()
        if not seller:
            seller = Sellers(item.get('seller_url'), item.get('seller_name'))
            self.db.session.add(seller)
            self.db.session.commit()

        address = self.db.session.query(Addresses).filter_by(address=item.get('address')).first()
        if not address:
            address = Addresses(item.get('address'))
            self.db.session.add(address)
            self.db.session.commit()

        images = [Images(img_item) for img_item in item.get('images')]

        ad = Flats(item.get('url'), item.get('title'), item.get('ad_type'), item.get('price'))
        ad.address = address.id
        ad.seller = seller.id
        ad.images = [img_id for img_id in images]
        self.db.session.add(ad)
        self.db.session.commit()
        print(1)
        return item
