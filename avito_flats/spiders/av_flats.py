# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class AvFlatsSpider(scrapy.Spider):
    name = 'av_flats'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/serpuhov/kvartiry?cd=1']

    def parse(self, response: HtmlResponse):
        next_link = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        ad_pages = response.xpath('//a[@class="item-description-title-link"]/@href').extract()

        for item in ad_pages:
            yield response.follow(item, callback = self.parse_ad_page)

        yield response.follow(next_link, callback=self.parse)

    def parse_ad_page(self, response: HtmlResponse):

        url = response.url
        title = response.xpath('//span[@class="title-info-title-text"]/text()').extract_first()
        ad_type = response.xpath('//span[@itemprop="itemListElement"]/a[@itemprop="item"]/@title').extract()[3]
        price = response.xpath('//span[@class="js-item-price"]/@content').extract_first()
        if ad_type == 'Снять':
            price += response.xpath('//span[contains(@class, "price-value-string")]/text()').extract()[-1].replace(u'\xa0', ' ').rstrip()
        images = response.xpath('//div[contains(@class, "js-gallery-img-frame")]/@data-url').extract()
        address = response.xpath('//span[@class="item-address__string"]/text()').extract_first().lstrip().rstrip()
        seller_url = response.xpath('//div[contains(@class, "seller-info-name")]/a/@href').extract_first().split('?')[0]
        seller_name = response.xpath('//div[contains(@class, "seller-info-name")]/a/text()').extract_first().lstrip().rstrip()

        yield {'url': url,
               'title': title,
               'ad_type': ad_type,
               'price': price,
               'images': images,
               'address': address,
               'seller_url': seller_url,
               'seller_name': seller_name,
               }
        #print(1)