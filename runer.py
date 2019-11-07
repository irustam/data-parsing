from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from config import INSTA_LOGIN, INSTA_PASS, users, query_hash
from insta import settings
from insta.spiders.insta_users import InstaUsersSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaUsersSpider, INSTA_LOGIN, INSTA_PASS, query_hash, users)
    process.start()