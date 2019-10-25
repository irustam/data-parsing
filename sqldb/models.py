from sqlalchemy import Table, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

associative_images = Table('associative_images', Base.metadata,
                           Column('flats', Integer, ForeignKey('flats.id')),
                           Column('images', Integer, ForeignKey('images.id'))
                           )

class Flats(Base):
    __tablename__ = 'flats'

    id = Column(Integer, primary_key = True, autoincrement = True)
    ad_url = Column(String, unique = True)
    title = Column(String)
    ad_type = Column(String)
    price = Column(String)
    address = Column(Integer, ForeignKey('addresses.id'))
    seller = Column(Integer, ForeignKey('sellers.id'))
    addresses = relationship('Addresses', backref = 'ads')
    sellers = relationship('Sellers', backref = 'ads')
    images = relationship('Images', secondary = associative_images, backref = 'ads')

    def __init__(self, ad_url, title, ad_type, price, address_id = None, seller_id = None, images = []):
        self.ad_url = ad_url
        self.title = title
        self.ad_type = ad_type
        self.price = price
        self.images.extend(images)
        self.address_id = address_id
        self.seller_id = seller_id

class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key = True, autoincrement = True)
    image_url = Column(String, unique = True)

    def __init__(self, image_url):
        self.image_url = image_url

class Addresses(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key = True, autoincrement = True)
    address = Column(String, unique = True)

    def __init__(self, address):
        self.address = address

class Sellers(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_url = Column(String, unique=True)
    seller_name = Column(String)

    def __init__(self, seller_url, seller_name):
        self.seller_url = seller_url
        self.seller_name = seller_name