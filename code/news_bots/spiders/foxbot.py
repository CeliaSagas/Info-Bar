import scrapy
from datetime import date
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


today=date.today()





class FOXpider(CrawlSpider):
    name = 'foxbot'
    allowed_domains = ['foxnews.com', 'foxbusiness.com']
    start_urls = ['https://www.foxnews.com']
    rules = [Rule(LinkExtractor(restrict_xpaths='//header/h2/a'),follow=False, callback='parse')]

    custom_settings ={
    'ITEM_PIPELINES':{
    'info_bar.pipelines.SavetoDB':1}
    }






    def parse(self, response):
        links = [response.url]


        for item in links:



            article_links = {
                'link':item
            }
            yield article_links
