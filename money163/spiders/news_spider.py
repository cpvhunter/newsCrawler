#encoding: utf-8
import scrapy
import re
from scrapy.selector import Selector
from money163.items import Money163Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
class ExampleSpider(CrawlSpider):
    name = "moneynews"
    allowed_domains = ["money.163.com"]

    def __init__(self, year='17', month='01', day='01', *args, **kwargs):        
        #allowrule = "/%s/%s\d+/\d+/*" % (year, month)
        allowrule = "/%s/%s%s/\d+/*" % (year, month, day)
        print(allowrule)
        
        ExampleSpider.rules=(Rule(LinkExtractor(allow=allowrule), callback="parse_news", follow=True),)
        #recompile the rule        
        super(ExampleSpider, self).__init__(*args, **kwargs)
           
    start_urls = ['http://money.163.com/', 'http://money.163.com/stock/']
    '''
        =Rule(LinkExtractor(allow=r"/\d+/*"),
                    callback="parse_news", follow=True
    )
    '''
    # f = open("out.txt", "w") 
    
    def printcn(suni):
        for i in suni:
            print(suni.encode('utf-8'))
    def parse_news(self,response):
        item = Money163Item()
        item['news_thread']=response.url.strip().split('/')[-1][:-5]
        # self.get_thread(response,item)
        self.get_title(response,item)
        self.get_source(response,item)
        self.get_url(response,item)
        self.get_news_from(response,item)
        self.get_from_url(response,item)
        self.get_text(response,item)
        return item##############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
    def get_title(self,response,item):
        title=response.xpath("/html/head/title/text()").extract()
        if title:
            # print ('title:'+title[0][:-5].encode('utf-8'))
            item['news_title']=title[0][:-5]

    def get_source(self,response,item):
        source=response.xpath("//div[@class='left']/text()").extract()
        if source:
            # print ('source'+source[0][:-5].encode('utf-8'))
            item['news_time']=source[0][:-5]

    def get_news_from(self,response,item):
        news_from=response.xpath("//div[@class='left']/a/text()").extract()
        if news_from:
            # print 'from'+news_from[0].encode('utf-8')        
            item['news_from']=news_from[0]

    def get_from_url(self,response,item):
        from_url=response.xpath("//div[@class='left']/a/@href").extract()
        if from_url:
            # print ('url'+from_url[0].encode('utf-8')        )
            item['from_url']=from_url[0]    

    def  get_text(self,response,item):
        news_body=response.xpath("//div[@id='endText']/p/text()").extract()
        if news_body:
            # for  entry in news_body:
            #     print (entry.encode('utf-8'))
            item['news_body']=news_body    
    def get_url(self,response,item):
        news_url=response.url
        if news_url:
            print (news_url)
        item['news_url']    =news_url

