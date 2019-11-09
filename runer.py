from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from config import INSTA_LOGIN, INSTA_PASS, users, query_hash
from zillow import settings
from zillow.spiders.re_zillow import ReZillowSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(InstaUsersSpider, INSTA_LOGIN, INSTA_PASS, query_hash, users)
    process.crawl(ReZillowSpider)
    process.start()