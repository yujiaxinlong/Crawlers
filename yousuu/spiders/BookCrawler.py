'''
Created on Jul 18, 2016

@author: yu
'''
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from yousuu.items import YousuuItem
from scrapy.http.request import Request
booklistNum = 0
pageNum = 0
class MySpider(CrawlSpider):
    name = 'yousuu'
    
    allowed_domains = ['yousuu.com']
    start_urls = ['http://www.yousuu.com/booklist']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
#         Rule(LinkExtractor(allow=('www.yousuu.com/booklist/\w*',)),
#                            callback = 'parse_booklist'),
             
#         Rule(LinkExtractor(allow=(), 
#             restrict_xpaths=('//a[contains(@onclick,"ys.common.jumpurl(\'t\'")]',)), 
#              callback="parse_next_page", follow= True),
#  
    )
#     def start_requests(self):
#         urls= []
#         url="http://www.yousuu.com/user/"
#         for i in range(900000):
#             urls.append(url+ str(i))
#         for url in urls:
#             yield Request(url, self.parse)
    def parse(self, response):
        global pageNum
        pageNum+=1
        print('xxxxxxxxxxxx')
        print(pageNum)
        # follow next page links
        hrefs = response.xpath('//a[contains(@href,"booklist/")]/@href').extract()
        for href in hrefs:
            new_url = "http://www.yousuu.com"+href
            yield scrapy.Request(new_url,callback=self.parse_booklist)
        next_page = response.xpath('//li/a').re('\'t\',\'\w*\'')[0].split(',')[1].strip("'")
        if next_page:
            next_page_url = "http://www.yousuu.com/booklist?t="+next_page
            request = scrapy.Request(url=next_page_url)
            yield request
    def parse_booklist(self, response):
        global booklistNum
        booklistNum+=1
        rsum=0
        nbOfBook = 0
        items = []
        userId = response.xpath("//div/a[contains(@href,'user')]/@href").extract_first()
        if userId == [] :
            userId = 0
        else:
            userId = userId.split('/')[2]
        for sel in response.xpath('//div[@class="mod"]'):
            bookId = sel.xpath('div/div[@class="title"]/a/@href').extract_first()
            if bookId == [] :
                bookId = 0
            else:
                bookId = bookId.split('/')[2]
            name= sel.xpath('div/div[@class="title"]/a/text()').extract()
            rating = sel.xpath(".//span[ @class = 'num2star' ]/text()").extract()
            if rating == [] :
                rating = 3.0
            else:
                rating = float(rating[0])
            rsum+=rating
            nbOfBook+=1
            item = YousuuItem({'userId':userId, 
                               'bookId':bookId,
                               'name':name,
                               'rating':rating,
                               'booklistNum':booklistNum})
            items.append(item)
#             item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
#             item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
#             item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        avgRating = rsum/nbOfBook
        
        for item in items:
            item['relativeRating']=round(item['rating']-avgRating,2)
            yield item
        split_url = response.url.split('?')
        booklist_url = split_url[0]
        if len(split_url)>1: 
            current_page = split_url[1].split('=')[1]
        else:
            current_page=1
        next_page = response.xpath('//li/a[contains(.,"»")]/@onclick').re('\d')
        if next_page != [] :
            if int(next_page[0])>int(current_page):
                next_page_url = response.url.split('?')[0] +"?page="+next_page[0]
                request = scrapy.Request(url=next_page_url,callback=self.parse_booklist)
                yield request 
