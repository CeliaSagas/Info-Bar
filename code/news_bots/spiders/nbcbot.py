import scrapy
from datetime import date
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


today=date.today()





class NBCSpider(CrawlSpider):
    name = 'nbcbot'
    allowed_domains = ['nbcnews.com']
    start_urls = ['https://www.nbcnews.com']
    rules = [Rule(LinkExtractor(restrict_xpaths='//div[2]/a'),follow=False, callback='parse')]

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
