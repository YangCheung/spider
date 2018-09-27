import scrapy
from diySpider.items import ThreadItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import os

username = os.environ.get("hipda-user") or "username"
pwd = os.environ.get("hipda-pwd") or "password"

class QuotesSpider(scrapy.Spider):
    name = "pda"
    startUrl = "https://www.hi-pda.com/forum/forumdisplay.php?fid=7&page=%s"
    page = 1
    HOST = "https://www.hi-pda.com/forum/"

    def start_requests(self):    
        request = scrapy.Request(url=((self.startUrl)%self.page), callback=self.parsePage)
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
                    'username': username,
                    'password': pwd,
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
        
    def parsePage(self, response):
        resultArray = response.xpath('//tbody[contains(@id, "normalthread_")]')
        for tempResult in resultArray:
            tid = tempResult.attrib.get('id')
            if tid and tid.startswith("normalthread_"):
                threadItem = ThreadItem()
                threadItem['tid'] = tid.replace("normalthread_", "")
                # print(tid)
                threadItem['title'] = tempResult.xpath('.//span[@id]/a/text()').extract_first()
                threadItem['turl'] = tempResult.xpath('.//span[@id]/a/@href').extract_first()    
                # print(title)
                # print(turl)

                threadItem['with_img_attach'] = len(tempResult.xpath('.//img[@alt="图片附件"]')) > 0
                # print("hasImageAttach %s"%hasImageAttach)
                threadItem['with_file_attach'] = len(tempResult.xpath('.//img[@alt="附件"]')) > 0
                # print("hasFileAttach %s"%hasFileAttach)

                threadItem['tag'] = tempResult.xpath('.//em[contains(text(), "[")]/a/text()').extract_first()    
                # print("tag %s"%tag)

                threadItem['author_uid'] = tempResult.xpath('.//td[@class="author"]//a/@href').re_first("uid=([0-9]+)")
                # print("authorUid %s"%authorUid)

                threadItem['author_username'] = tempResult.xpath('.//td[@class="author"]//a/text()').extract_first()    
                # print("author %s"%authorName)
                
                threadItem['publish_date'] = tempResult.xpath('.//td[@class="author"]/em/text()').extract_first()    
                # print("%s"%publishDate)

                postCount = tempResult.xpath('.//td[@class="nums"]/strong/text()').extract_first()    
                try:
                    postCount = int(postCount)
                except ValueError as e:
                    postCount = -1
                threadItem['follow_post_count'] = postCount
                # print("postCount = %s"%int(postCount))

                readCount = tempResult.xpath('.//td[@class="nums"]/em/text()').extract_first()    
                try:
                    readCount = int(readCount)
                except ValueError as e:
                    readCount = -1
                threadItem['read_count'] = readCount
                # print("readCount = %s"%readCount)

                threadItem['last_post_username'] = tempResult.xpath('.//td[@class="lastpost"]/cite/a/text()').extract_first()    
                # print("lastPostUser = %s"%lastPostUser)

                threadItem['last_post_date'] = tempResult.xpath('.//td[@class="lastpost"]/em/a/text()').extract_first()    
                # print("lastPostDate = %s"%lastPostDate)
                print(threadItem)
                print("================")
                yield threadItem

                self.page += 1

        nextPage = response.xpath('//a[@class="next"]/@href').extract_first()
        if nextPage:
            request = scrapy.Request(url=("%s%s")%(self.HOST, nextPage), callback=self.parsePage)
            yield request


            
        
        

