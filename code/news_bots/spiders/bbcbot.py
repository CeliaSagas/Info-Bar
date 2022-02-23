import scrapy
from datetime import date
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

today=date.today()





class BBCSpider(CrawlSpider):
    name = 'bbcbot'
    allowed_domains = ['bbc.com', 'bbc.co.uk']
    start_urls = ['https://www.bbc.com/news']
    rules = [Rule(LinkExtractor(restrict_xpaths='//div[2]/div/a'),follow=False, callback='parse')]

    custom_settings ={
    'ITEM_PIPELINES':{
    'info_bar.pipelines.SavetoDB':1}
    }






    def parse(self, response):
        links = set(response.xpath('//a[contains(@href,"bbc.co.uk/news/")]/@href').extract())


        for item in links:

            if "help" in item:
                pass

            else:
                article_links = {
                    'link':item
                }
                yield article_links
