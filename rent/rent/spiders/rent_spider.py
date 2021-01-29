import scrapy
from rent.items import RentItem
import re

class RentSpider(scrapy.Spider):
    name = 'rent'
    allowed_domains=['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/dongcheng/pg1']

    def parse(self, response):
        # crawl
        houses = response.css('.content__list--item')
        for house in houses:
            item = RentItem()
            item['link'] = house.css('a::attr(href)').get()
            item['title'] = house.css('a::attr(title)').get()
            item['photo'] = house.css('a').css('img::attr(src)').get()
            item['location'] = house.css('.content__list--item--des').css('a::text').getall()
            infos = house.css('.content__list--item--des::text').getall()
            if len(infos) > 7:
                item['area'] = infos[4].strip()
                item['direction'] = infos[5].strip()
                item['rooms'] = infos[6].strip()
            item['price'] = house.css('.content__list--item-price').css('em::text').get()
            yield item
        
        if response.css(".content__pg") != None:
            total_page = int(response.css(".content__pg::attr(data-totalpage)").get())
            current_page = int(response.css(".content__pg::attr(data-curpage)").get())
            if current_page < total_page:
                last_url = response.request.url
                m = re.match(r'(.*?)(pg\d+)(.*)', last_url)
                next_url = m.group(1) + "pg" + str(current_page+1) + m.group(3)
                yield scrapy.Request(url=next_url, callback=self.parse)    