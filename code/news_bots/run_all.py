import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('bbcbot', domain=['bbc.com', 'bbc.co.uk'])
process.crawl('breitbot', domain='https://www.breitbart.com')
process.crawl('foxbot', domain=['foxnews.com', 'foxbusiness.com'])
process.crawl('nbcbot', domain='nbcnews.com')
process.crawl('timesbot', domain='https://www.nytimes.com')
process.start()
