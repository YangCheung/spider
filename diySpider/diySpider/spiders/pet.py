import scrapy
from diySpider.items import PetItem, PetArticleItem

class PetSpider(scrapy.Spider):
    name = "pet"
    HOST = "http://www.ixiupet.com/pinzhong/"

    def start_requests(self):
        urls = [
            { "url" : 'http://www.ixiupet.com/ggpz/', "category" : 'dog' },
            { "url" : 'http://www.ixiupet.com/mmpz/', "category" : 'cat' },
            { "url" : 'http://www.ixiupet.com/tzpz/', "category" : 'rabbit' },
            { "url" : 'http://www.ixiupet.com/ccpz/', "category" : 'bug' },
            { "url" : 'http://www.ixiupet.com/szpz/', "category" : 'aquatic' },
            { "url" : 'http://www.ixiupet.com/cwspz/', "category" : 'rat' },
            { "url" : 'http://www.ixiupet.com/cwdpz/', "category" : 'diao' },
            { "url" : 'http://www.ixiupet.com/cwnpz/', "category" : 'bird' },
            { "url" : 'http://www.ixiupet.com/pxpz/', "category" : 'paxing' },
            { "url" : 'http://www.ixiupet.com/llpz/', "category" : 'linglei' }
        ]
        for url in urls:
            request = scrapy.Request(url=url["url"], callback=self.parse)
            request.meta['category'] = url["category"]
            request.meta['origin'] = url["url"]
            yield request

    def parse(self, response):
        resultArray = response.css("a[class=tiyan-smll-li]")
        category = response.meta["category"]
        for tempResult in resultArray:
            item = PetItem()
            item["category"] = category
            item["url"] = tempResult.xpath("@href").extract_first()
            item["cover"] = tempResult.css("img").xpath('@src').extract_first()
            item["name"] = tempResult.css("img").xpath('@title').extract_first()
            request = scrapy.Request(url = item["url"], callback = self.parsePage)
            request.meta['item'] = item
            yield request

        nextPage = response.css("a[class=next]").xpath("@href").extract_first()
        if nextPage and nextPage != "":
            nextPage = ("%s%s"%(response.meta["origin"], nextPage))
            self.log('next page = %s' % (nextPage))
            request = scrapy.Request(url = nextPage, callback = self.parse)
            request.meta['category'] = category
            request.meta['origin'] = response.meta["origin"]
            yield request
        
    def parsePage(self, response):
        item = response.meta['item']
        # self.log('item = %s'%item)
        item['images'] = response.xpath("//a[@class='fancybox']/img/@src").extract()
        item['likeNum'] = response.xpath("//dl[@class='rs1']//em/text()").extract_first()
        item['wantPetNum'] = response.xpath("//dl[@class='rs3']//em/text()").extract_first()
        item['price'] = response.xpath("//span[@class='cankao']//strong/text()").extract_first()

        # attrs = response.xpath("//ul[@class='c1text3']//li")
        item['xueming'] = response.xpath('//li[contains(text(), "中文学名")]//a/text()').extract_first()
        item['bieming'] = response.xpath('//li[contains(text(), "别　　名")]//a/text()').extract_first()
        item['fenbuquyu'] = response.xpath('//li[contains(text(), "分布区域")]//a/text()').extract_first()
        item['yuanchandi'] = response.xpath('//li[contains(text(), "原 产 地")]//a/text()').extract_first()
        item['tixing'] = response.xpath('//li[contains(text(), "体　　型")]//a/text()').extract_first()
        item['shengao'] = response.xpath('//li[contains(text(), "身　　高")]//a/text()').extract_first()
        item['weight'] = response.xpath('//li[contains(text(), "体　　重")]//a/text()').extract_first()
        item['lifeTime'] = response.xpath('//li[contains(text(), "寿　　命")]//a/text()').extract_first()

        # 粘人程度
        item['nianren'] = response.xpath('//li/span[contains(text(), "粘 人 程 度")]/parent::li/div/@class').extract_first()
        # 喜 叫 程 度
        item['xijiao'] = response.xpath('//li/span[contains(text(), "喜 叫 程 度")]/parent::li/div/@class').extract_first()
        # 友 善 程 度
        item['youshan'] = response.xpath('//li/span[contains(text(), "友 善 程 度")]/parent::li/div/@class').extract_first()
        # 掉 毛 程 度
        item['diaomao'] = response.xpath('//li/span[contains(text(), "掉 毛 程 度")]/parent::li/div/@class').extract_first()
        # 美容程度
        item['meirong'] = response.xpath('//li/span[contains(text(), "美容程度")]/parent::li/div/@class').extract_first()
        # 体味程度
        item['tiwei'] = response.xpath('//li/span[contains(text(), "体味程度")]/parent::li/div/@class').extract_first()
        # 口水程度
        item['koushui'] = response.xpath('//li/span[contains(text(), "口水程度")]/parent::li/div/@class').extract_first()
        # 可训程度
        item['xunlian'] = response.xpath('//li/span[contains(text(), "可训程度")]/parent::li/div/@class').extract_first()
        # 活跃
        item['huoyue'] = response.xpath('//li/span[contains(text(), "活跃程度")]/parent::li/div/@class').extract_first()
        # 城市程度
        item['chengshi'] = response.xpath('//li/span[contains(text(), "城市适度")]/parent::li/div/@class').extract_first()
        # 耐寒程度
        item['naihan'] = response.xpath('//li/span[contains(text(), "耐寒程度")]/parent::li/div/@class').extract_first()
        # 耐热程度
        item['naire'] = response.xpath('//li/span[contains(text(), "耐热程度")]/parent::li/div/@class').extract_first()
        # 运动程度
        item['yundong'] = response.xpath('//li/span[contains(text(), "运动程度")]/parent::li/div/@class').extract_first()
        
        desc_names = response.xpath('//ul[@class="con2list"]//li/a/text()')
        desc_values = response.xpath('//div[@class="quanjieshao1"]')
        desc_count = min(len(desc_names), len(desc_values))
        
        i = 0
        descs = []
        while(i < desc_count):
            desc_name = desc_names[i].extract()
            if desc_name == "萌图推荐":
                image_articles_res = desc_values[i].xpath('*//li')
                image_articles = []
                for image_article_res in image_articles_res:
                    image_title = image_article_res.xpath('a[@class="tiyan-smll-li"]/@title').extract_first()
                    image_article_url = image_article_res.xpath('a[@class="tiyan-smll-li"]/@href').extract_first()
                    image_url = image_article_res.xpath('*//img/@src').extract_first()
                    image_articles.append({
                        "image_title": image_title,
                        "image_article_url": image_article_url,
                        "image_url": image_url 
                        })
                    articleRequet = scrapy.Request(url = image_article_url, callback = self.parsePetArticle)
                    yield articleRequet
                # self.log(' %s' % (image_articles))
                item['image_articles'] = image_articles
            else:
                desc_value = desc_values[i].extract()
                descs.append({
                   desc_name: desc_value
                })
            i = i + 1
        item["descs"] = descs
        # self.log(' %s' % (item["images"]))
        yield item

    def parsePetArticle(self, response):
        articleItem = PetArticleItem()
        articleItem["url"] = response.url
        articleItem["content"] = response.xpath("//div[@class='article-content']").extract()
        yield articleItem
        
        

