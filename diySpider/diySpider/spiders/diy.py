import scrapy
from diySpider.items import DiyItem

class QuotesSpider(scrapy.Spider):
    name = "diy"
    HOST = "https://ertong.rouding.com"

    def start_requests(self):
        urls = [
            { "url": 'https://ertong.rouding.com/diy/', "category" : 'diy' },
            { "url" :'https://ertong.rouding.com/ertonghua/', "category" : 'ertonghua' },
            { "url" : 'https://ertong.rouding.com/kexue/', "category" : 'kexue' },
            { "url" : 'https://ertong.rouding.com/xt/', "category" : 'youerjiaoan' },
            { "url" :'https://ertong.rouding.com/qinzi/', "category" : 'qinzi' },
            { "url" : 'https://ertong.rouding.com/gushi/', "category" : 'gushi' }
        ]
        for url in urls:
            request = scrapy.Request(url=url["url"], callback=self.parse)
            request.meta['category'] = url["category"]
            yield request

    def parse(self, response):
        resultArray = response.css("div[class=all]").css("a")
        nextPage = response.xpath('//a[contains(text(), ">")]/@href').extract_first()
        category = response.meta["category"]
        self.log('next page = %s' % (nextPage))
        for tempResult in resultArray:
            item = DiyItem()
            item["category"] = category
            url = tempResult.xpath("@href").extract_first()
            item["url"] = url
            backgroundImg = tempResult.re_first(r"\(.*\)")
            if backgroundImg:
                item["backgroundImg"] = "https://%s"%(backgroundImg.replace("(//", "").replace(")", ""))
            item["title"] = tempResult.css("div[class=x7]::text").extract_first()
            item["desc"] = tempResult.css("div[class=x8]::text").extract_first()
            request = scrapy.Request(url = ("%s%s"%(self.HOST, url)), callback = self.parsePage)
            request.meta['item'] = item
            yield request

        if nextPage and nextPage != "#":
            request = scrapy.Request(url = ("%s%s"%(self.HOST, nextPage)), callback = self.parse)
            request.meta['category'] = category
            yield request
        
    def parsePage(self, response):
        item = response.meta['item']
        self.log('item = %s'%item)
        article = response.css("div[id=zoom]").extract_first()
        if article:
            item["article"] = article
            yield item
        
        

