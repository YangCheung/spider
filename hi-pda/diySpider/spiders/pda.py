import scrapy
from diySpider.items import DiyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

class QuotesSpider(scrapy.Spider):
    name = "pda"
    HOST = "https://ertong.rouding.com"

    def start_requests(self):    
        request = scrapy.Request(url="https://www.hi-pda.com/forum/forumdisplay.php?fid=7&page=1", callback=self.parsePage)
        yield request

    # def start_requests(self):
    #     return [Request("https://www.hi-pda.com/forum/logging.php?action=login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        return [FormRequest.from_response(
                response,   
                "https://www.hi-pda.com/forum/logging.php?action=login&loginsubmit=yes",
                meta = {'cookiejar' : response.meta['cookiejar']},
                # headers = self.headers,
                formdata = {
                    'loginfield': 'username',
                    'username': 'sadsea',
                    'password': 'b6882e4d39e32c1cf596016f943cd73b',
                    'questionid': '0',
                    'answer': ''
                },
                callback = self.after_login,
                dont_filter = True
            )]

    def after_login(self, response):
        request = scrapy.Request(
            url = 'https://www.hi-pda.com/forum/forumdisplay.php?fid=2&page=1', 
            meta = {'cookiejar' : response.meta['cookiejar']}, 
            callback = self.parsePage
            )
        yield request
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
        
    def parsePage(self, response):
        # resultArray = response.css("tbody")
        resultArray = response.xpath('//tbody[contains(@id, "normalthread")]')
        # print(resultArray.extract())
        for tempResult in resultArray:
            tid = tempResult.attrib.get('id')
            # print(tid)
            title = tempResult.xpath('.//span/a/text()').extract_first()
            turl = tempResult.xpath('.//span/a/@href').extract_first()    
            print(title)
            print(turl)

            hasImageAttach = len(tempResult.xpath('.//img[@alt="图片附件"]')) > 0
            print("hasImageAttach %s"%hasImageAttach)
            hasFileAttach = len(tempResult.xpath('.//img[@alt="附件"]')) > 0
            print("hasFileAttach %s"%hasFileAttach)

            tag = tempResult.xpath('.//em[contains(text(), "[")]/a/text()').extract_first()    
            print("tag %s"%tag)

            author = tempResult.xpath('.//td[@class="author"]//a/text()').extract_first()    
            print("author %s"%author)
            
            publishDate = tempResult.xpath('.//td[@class="author"]/em/text()').extract_first()    
            print("%s"%publishDate)

            postCount = tempResult.xpath('.//td[@class="nums"]/strong/text()').extract_first()    
            try:
                postCount = int(postCount)
            except ValueError as e:
                postCount = -1
            print("postCount = %s"%int(postCount))

            readCount = tempResult.xpath('.//td[@class="nums"]/em/text()').extract_first()    
            try:
                readCount = int(readCount)
            except ValueError as e:
                readCount = -1
            print("readCount = %s"%readCount)

            lastPostUser = tempResult.xpath('.//td[@class="lastpost"]/cite/a/text()').extract_first()    
            print("lastPostUser = %s"%lastPostUser)

            lastPostDate = tempResult.xpath('.//td[@class="lastpost"]/em/a/text()').extract_first()    
            print("lastPostDate = %s"%lastPostDate)
            print("================")
            
            # tid = tempResult.xpath("//tbody/@id").extract_first()
            # print("tid = %s"%tid)
        # article = response.css("div[id=zoom]").extract_first()
        # if article:
        #     item["article"] = article
        #     yield item
        
        

