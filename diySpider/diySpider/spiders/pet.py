import scrapy
from diySpider.items import PetCategory

class PetSpider(scrapy.Spider):
    name = "pet"
    HOST = "http://www.ixiupet.com/pinzhong/"

    def start_requests(self):
        urls = [
            { "url" : 'http://www.ixiupet.com/ggpz/', "category" : 'dog' },
            # { "url" : 'http://www.ixiupet.com/mmpz/', "category" : 'cat' },
            # { "url" : 'http://www.ixiupet.com/tzpz/', "category" : 'rabbit' },
            # { "url" : 'http://www.ixiupet.com/ccpz/', "category" : 'bug' },
            # { "url" : 'http://www.ixiupet.com/szpz/', "category" : 'aquatic' },
            # { "url" : 'http://www.ixiupet.com/cwspz/', "category" : 'rat' },
            # { "url" : 'http://www.ixiupet.com/cwdpz/', "category" : 'diao' },
            # { "url" : 'http://www.ixiupet.com/cwnpz/', "category" : 'bird' },
            # { "url" : 'http://www.ixiupet.com/pxpz/', "category" : 'paxing' },
            # { "url" : 'http://www.ixiupet.com/llpz/', "category" : 'linglei' }
        ]
        for url in urls:
            request = scrapy.Request(url=url["url"], callback=self.parse)
            request.meta['category'] = url["category"]
            yield request

    def parse(self, response):
        resultArray = response.css("p[class=tiyan-smll-li]").css("a")
        nextPage = response.css("a[class=next]").xpath("@href").extract_first()
        category = response.meta["category"]
        self.log('next page = %s' % (nextPage))
        for tempResult in resultArray:
            item = PetCategory()
            item["category"] = category
            item["url"] = tempResult.xpath("@href").extract_first()
            item["cover"] = tempResult.css("img").xpath('@src').extract_first()
            item["title"] = tempResult.css("img").xpath('@title').extract_first()
            request = scrapy.Request(url = item["url"], callback = self.parsePage)
            request.meta['item'] = item
            yield request

        # if nextPage and nextPage != "#":
        #     request = scrapy.Request(url = ("%s%s"%(self.HOST, nextPage)), callback = self.parse)
        #     request.meta['category'] = category
        #     yield request
        
    def parsePage(self, response):
        item = response.meta['item']
        self.log('item = %s'%item)

        likeNum = response.xpath("//dl[@class='rs1']//em/text()").extract_first()
        wantPetNum = response.xpath("//dl[@class='rs3']//em/text()").extract_first()
        price = response.xpath("//span[@class='cankao']//strong/text()").extract_first()

        # attrs = response.xpath("//ul[@class='c1text3']//li")
        xueming = response.xpath('//li[contains(text(), "中文学名")]//a/text()').extract_first()
        bieming = response.xpath('//li[contains(text(), "别　　名")]//a/text()').extract_first()
        fenbuquyu = response.xpath('//li[contains(text(), "分布区域")]//a/text()').extract_first()
        yuanchandi = response.xpath('//li[contains(text(), "原 产 地")]//a/text()').extract_first()
        tixing = response.xpath('//li[contains(text(), "体　　型")]//a/text()').extract_first()
        shengao = response.xpath('//li[contains(text(), "身　　高")]//a/text()').extract_first()
        weight = response.xpath('//li[contains(text(), "体　　重")]//a/text()').extract_first()
        lifeTime = response.xpath('//li[contains(text(), "寿　　命")]//a/text()').extract_first()

        # 粘人程度
        nianren = response.xpath('//li/span[contains(text(), "粘 人 程 度")]/parent::li/div/@class').extract_first()
        # 喜 叫 程 度
        xijiao = response.xpath('//li/span[contains(text(), "喜 叫 程 度")]/parent::li/div/@class').extract_first()
        # 友 善 程 度
        youshan = response.xpath('//li/span[contains(text(), "友 善 程 度")]/parent::li/div/@class').extract_first()
        # 掉 毛 程 度
        diaomao = response.xpath('//li/span[contains(text(), "掉 毛 程 度")]/parent::li/div/@class').extract_first()
        # 美容程度
        meirong = response.xpath('//li/span[contains(text(), "美容程度")]/parent::li/div/@class').extract_first()
        # 体味程度
        tiwei = response.xpath('//li/span[contains(text(), "体味程度")]/parent::li/div/@class').extract_first()
        # 体味程度
        koushui = response.xpath('//li/span[contains(text(), "口水程度")]/parent::li/div/@class').extract_first()
        # 可训程度
        xunlian = response.xpath('//li/span[contains(text(), "可训程度")]/parent::li/div/@class').extract_first()
        # 活跃
        huoyue = response.xpath('//li/span[contains(text(), "活跃程度")]/parent::li/div/@class').extract_first()
        # 城市程度
        chengshi = response.xpath('//li/span[contains(text(), "城市程度")]/parent::li/div/@class').extract_first()
        # 耐寒程度
        naihan = response.xpath('//li/span[contains(text(), "耐寒程度")]/parent::li/div/@class').extract_first()
        # 耐热程度
        naire = response.xpath('//li/span[contains(text(), "耐热程度")]/parent::li/div/@class').extract_first()
        # 运动程度
        yundong = response.xpath('//li/span[contains(text(), "运动程度")]/parent::li/div/@class').extract_first()
        

        desc_names = response.xpath('//ul[@class="con2list"]//li/a/text()')
        desc_values = (response.xpath('//div[@class="quanjieshao1"]')
        desc_count = min(len(desc_names), len(desc_values))
        i = 0
        while(i < desc_count):
            desc_name = desc[i].extract()
            desc_value = desc_values[i].extract()
            i = i + 1
            self.log(' %s' % (desc_name))
            self.log(' %s' % (desc_value))

        # if article:
        #     item["article"] = article
        #     yield item
        
        

