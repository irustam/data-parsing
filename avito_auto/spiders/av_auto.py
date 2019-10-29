# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from avito_auto.items import AvitoAutoItem
from scrapy.crawler import CrawlerProcess
from avito_auto.items import cleaner_dict_data
import json

class AvAutoSpider(scrapy.Spider):
    name = 'av_auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/serpuhov/avtomobili?cd=1&radius=0']
    #start_urls = ['https://m.avito.ru/serpuhov/avtomobili/chevrolet_niva_2005_1269542389']
    page = 1

    def parse(self, response: HtmlResponse):
        next_link = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        ad_pages = response.xpath('//a[@class="item-description-title-link"]/@href').extract()

        for item in ad_pages:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53',
            }
            item = 'https://m.avito.ru' + item
            yield response.follow(item, callback=self.parse_ad_page, headers=headers)

        yield response.follow(next_link, callback=self.parse)

    def parse_ad_page(self, response: HtmlResponse):
        ad_data = response.xpath('//script[@type="text/javascript"]').extract()
        ad_data = cleaner_dict_data(ad_data)
        images = ad_data.pop('images')

        cb_kwargs = {'ad_data': ad_data,
                     'ad_url': response.url,
                     'images': images
                    }

        link_other_props = f'https://www.avito.ru/js/items/{ad_data["id"]}/car_spec'
        print(1)

        yield response.follow(link_other_props, callback=self.parse_props, cb_kwargs=cb_kwargs)

    def parse_props(self, response: HtmlResponse, ad_data, ad_url, images):
        props_data = json.loads(response.body)
        cb_kwargs = {'ad_data': ad_data,
                     'ad_url': ad_url,
                     'images': images,
                     'props_data': props_data,
                    }
        link_vin = f'https://www.avito.ru/web/1/swaha/v1/autoteka/teaser/{ad_data["id"]}?unlockCrashes=true'
        print(2)
        yield response.follow(link_vin, callback=self.parse_vin, cb_kwargs=cb_kwargs)


    def parse_vin(self, response: HtmlResponse, ad_data, ad_url, images, props_data):
        vin_data = json.loads(response.body)

        item = ItemLoader(AvitoAutoItem(), response)
        item.add_value('url', ad_url)
        item.add_value('data', ad_data)
        item.add_value('images', images)
        item.add_value('properties', props_data)
        item.add_value('vin_data', vin_data)
        print(3)
        yield item.load_item()


