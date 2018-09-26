import scrapy
from scrapy.selector import Selector
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule

from PTSpider.items import DiyItem

class QuotesSpider(scrapy.Spider):
    name = "PT"
    HOST = "https://totheglory.im"
    allowed_domains = ["totheglory.im"]

    start_urls = [
        "https://totheglory.im/browse.php?search_field=&c=M&&page=0&"
    ]
    # rules = (
    #     Rule(SgmlLinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
    #     Rule(SgmlLinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
    # )
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Referer": "https://totheglory.im"
    }

    #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [Request("https://totheglory.im/login.php?returnto=", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        print('Preparing login')
        
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response, "https://totheglory.im/login.php",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,  #注意此处的headers
                            formdata = {
                                'username': "",
                                'password': '',
                                'otp': '',
                                'passan': '',
                                'passid': '0',
                                'lang': '0',
                                'rememberme': 'no'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]

    def after_login(self, response) :
        for url in self.start_urls :
            yield scrapy.Request(url, callback=self.parse)

    # def parse_page(self, response):
    #     problem = Selector(response)
    #     item = ZhihuItem()
    #     item['url'] = response.url
    #     item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
    #     print item['name']
    #     item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
    #     item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
    #     item['answer']= problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
    #     return item

    def parse(self, response):
        print(response)
        # resultArray = response.css("div[class=all]").css("a")
        # nextPage = response.xpath('//a[contains(text(), ">")]/@href').extract_first()
        # category = response.meta["category"]
        # self.log('next page = %s' % (nextPage))
        # for tempResult in resultArray:
        #     item = DiyItem()
        #     item["category"] = category
        #     url = tempResult.xpath("@href").extract_first()
        #     item["url"] = url
        #     backgroundImg = tempResult.re_first(r"\(.*\)")
        #     if backgroundImg:
        #         item["backgroundImg"] = "https://%s"%(backgroundImg.replace("(//", "").replace(")", ""))
        #     item["title"] = tempResult.css("div[class=x7]::text").extract_first()
        #     item["desc"] = tempResult.css("div[class=x8]::text").extract_first()
        #     request = scrapy.Request(url = ("%s%s"%(self.HOST, url)), callback = self.parsePage)
        #     request.meta['item'] = item
        #     yield request

        # if nextPage and nextPage != "#":
        #     request = scrapy.Request(url = ("%s%s"%(self.HOST, nextPage)), callback = self.parse)
        #     request.meta['category'] = category
        #     yield request
        
    # def parsePage(self, response):
    #     item = response.meta['item']
    #     self.log('item = %s'%item)
    #     article = response.css("div[id=zoom]").extract_first()
    #     if article:
    #         item["article"] = article
    #         yield item
        
        

