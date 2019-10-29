from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito_auto import settings
from avito_auto.spiders.av_auto import AvAutoSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(AvAutoSpider)
    process.start()