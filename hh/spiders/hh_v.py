# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class HhVSpider(scrapy.Spider):
    name = 'hh_v'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80+%D0%BF%D0%BE+%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D1%83&items_on_page=100']

    def parse(self, response: HtmlResponse):
        next_link = response.css('a.bloko-button.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()
        v_pages = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()

        for item in v_pages:
            v_page = item.split('?')[0]
            yield response.follow(v_page, callback = self.parse_v_page)

        yield response.follow(next_link, callback=self.parse)

    def parse_v_page(self, response: HtmlResponse):
        title = response.css('div.vacancy-title h1::text').extract_first()
        company_hh_page = response.css('a.vacancy-company-name::attr(href)').extract_first().split('?')[0]
        company_name = response.css('a.vacancy-company-name span::text').extract_first()
        salary = response.css('p.vacancy-salary::text').extract_first().replace(u'\xa0', ' ')
        skills = response.css('span.bloko-tag.bloko-tag_inline.Bloko-TagList-Tag::attr(data-tag-id)').extract()

        yield response.follow(company_hh_page, callback = self.parse_company_page)
        yield {'title': title,
               'salary': salary,
               'skills': skills,
               'company_hh_page': company_hh_page,
               }
        yield {'company_hh_page': company_hh_page,
               'company_name': company_name,
               }

    def parse_company_page(self, response: HtmlResponse):
        link = response.css('a.company-url::attr(href)').extract_first()
        link2 = response.css('a.tmpl_hh_head__link::attr(href)').extract_first()
        company_page = response.url.split('//')[1].split('/')
        company_hh_page = '/' + company_page[1] + '/' + company_page[2].split('?')[0]

        yield {'company_hh_page': company_hh_page,
               'company_url': link or link2,
               }