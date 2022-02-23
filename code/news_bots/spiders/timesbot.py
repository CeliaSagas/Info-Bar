import scrapy
from datetime import date

today=date.today()

# breitbart uses yy/mm/dd
string_ = today.strftime("%y/%m/%d")




class NYTimesSpider(scrapy.Spider):
    name = 'timesbot'
    allowed_domains = ['https://www.nytimes.com']
    start_urls = ['https://www.nytimes.com']

    custom_settings ={
    'ITEM_PIPELINES':{
    'info_bar.pipelines.SavetoDB':1}
    }


    def parse(self,response):

        links = set(response.xpath('//a[contains(@href,"'+string_+'")]/@href').extract())

        for item in links:
            if item.endswith("/#disqus_thread"):
                pass
            elif item[0]=="/":
                pass
            else:
                article_links = {
                    'link':item
                }
                yield article_links
