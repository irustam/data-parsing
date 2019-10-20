from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hh import settings
from hh.spiders.hh_v import HhVSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(HhVSpider)
    process.start()