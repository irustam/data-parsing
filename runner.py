from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_flats import settings
from avito_flats.spiders.av_flats import AvFlatsSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(AvFlatsSpider)
    process.start()