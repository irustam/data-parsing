# -*- coding: utf-8 -*-
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from zillow.items import ZillowItem
from urllib.parse import urlencode, urljoin


class ReZillowSpider(scrapy.Spider):
    name = 're_zillow'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['https://www.zillow.com/fort-worth-tx/']
    browser = webdriver.Firefox()

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//li[@class="zsg-pagination-next"]/a[@aria-label="NEXT Page"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        ads = response.xpath('//ul[contains(@class, "photo-cards")]/li/article/a/@href').extract()
        for ad in ads:
            yield response.follow(ad, callback=self.parse_ad)

    def parse_ad(self, response:HtmlResponse):
        self.browser.get(response.url)
        time.sleep(2)

        #Собираем ссылкии на картинки
        media = self.browser.find_element_by_css_selector('.ds-media-col')
        media_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
        images = ''
        if media_len:
            while True:
                media.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                media.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                media.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                media.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                media.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                tmp_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
                if tmp_len == media_len:
                    break
                media_len = len(self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))
            images = [itm.get_attribute('srcset').split(' ')[-2] for itm in
                      self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
                      ]

        #Получаем данные о доме за кнопкой "Показать больше"
        #Кликаем по кнопке
        buttons_show_more = self.browser.find_elements_by_xpath('//div[contains(@class, "Card")]/div/a')[0]
        buttons_show_more.click()
        time.sleep(1)

        #Берем все div из блока, который нам открылся по кнопке и проходимся по нему для сбора параметров недвижимости
        facts_more = self.browser.find_elements_by_xpath('//div[@class="ds-expandable-card-expanded"]/div')
        block_result = {}
        if len(facts_more):
            for block in facts_more:
                if block.get_attribute('class')[:6] != 'Spacer':
                    try:
                        header = block.find_element_by_xpath('//h5').text
                        facts_sub_blocks = block.find_elements_by_xpath('div/div')
                    except NoSuchElementException:
                        header = block.find_element_by_xpath('div/div[contains(@class, "header")]').text
                        facts_sub_blocks = block.find_elements_by_xpath('div/ul/li')


                    sub_block_result = {}
                    if len(facts_sub_blocks):
                        for sub_block in facts_sub_blocks:
                            facts = []
                            try:
                                sub_header = sub_block.find_element_by_xpath('span').text
                                facts_list = sub_block.find_elements_by_xpath('ul/li/span')
                                if len(facts_list):
                                    for itm in facts_list:
                                        facts.append(itm.text)
                            except NoSuchElementException:
                                sub_header = sub_block.find_element_by_xpath('div[contains(@class, "title")]').text
                                facts_list = sub_block.find_elements_by_xpath('table/tbody/tr')
                                if len(facts_list):
                                    for itm in facts_list:
                                        key_value = itm.find_elements_by_xpath('td')
                                        facts.append(key_value[0].text + ': ' + key_value[1].text)
                            sub_block_result.update({sub_header: facts})
                    block_result.update({header: sub_block_result})
        item = ItemLoader(ZillowItem(), response)

        # Собираем доступные скрапи данные со страницы и отправляем в item:
        item.add_value('url', response.url)
        item.add_xpath('address', '//h1[@class="ds-address-container"]/span/text()')
        item.add_xpath('price', '//h3[@class="ds-price"]/span/span[@class="ds-value"]/text()')
        item.add_xpath('zestimate_price', '//span[@class="ds-estimate"]/span/span[@class="ds-estimate-value"]/text()')
        item.add_xpath('description', '//div[@class="ds-overview-section"]/div[contains(@class, "Text-sc")]/text()')
        item.add_xpath('facts_and_features', '//ul[@class="ds-home-fact-list"]/li/span/text()')
        item.add_value('facts_and_features_more', block_result)
        item.add_value('images', images)
        yield item.load_item()

        print(2)
