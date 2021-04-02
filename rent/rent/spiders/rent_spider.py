import scrapy
from rent.items import RentItem
import re

class RentSpider(scrapy.Spider):
    name = 'rent'
    allowed_domains=['bj.lianjia.com']
    start_urls = [
        'https://bj.lianjia.com/zufang/dongcheng/pg1rco11/',
        'https://bj.lianjia.com/zufang/xicheng/pg1rco11/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11rp1rp2rp3rp4/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11l0rp5/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11l1rp5/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11l2l3rp5/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11l0l1rp6/',
        'https://bj.lianjia.com/zufang/chaoyang/pg1rco11l2l3rp6/',
        'https://bj.lianjia.com/zufang/haidian/pg1rco11l0/',
        'https://bj.lianjia.com/zufang/haidian/pg1rco11l1/',
        'https://bj.lianjia.com/zufang/haidian/pg1rco11l2l3/',
        'https://bj.lianjia.com/zufang/fengtai/pg1rco11l0/',
        'https://bj.lianjia.com/zufang/fengtai/pg1rco11l1/',
        'https://bj.lianjia.com/zufang/fengtai/pg1rco11l2l3/',
        'https://bj.lianjia.com/zufang/shijingshan/pg1rco11/',
        'https://bj.lianjia.com/zufang/tongzhou/pg1rco11l0l1/',
        'https://bj.lianjia.com/zufang/tongzhou/pg1rco11l2l3/',
        'https://bj.lianjia.com/zufang/changping/pg1rco11/',
        'https://bj.lianjia.com/zufang/daxing/pg1rco11l0/',
        'https://bj.lianjia.com/zufang/daxing/pg1rco11l1/',
        'https://bj.lianjia.com/zufang/daxing/pg1rco11l2l3/',
        'https://bj.lianjia.com/zufang/yizhuangkaifaqu/pg1rco11/',
        'https://bj.lianjia.com/zufang/shunyi/pg1rco11/',
        'https://bj.lianjia.com/zufang/fangshan/pg1rco11/',
        'https://bj.lianjia.com/zufang/mentougou/pg1rco11/',
        'https://bj.lianjia.com/zufang/pinggu/pg1rco11/',
        'https://bj.lianjia.com/zufang/huairou/pg1rco11/',
        'https://bj.lianjia.com/zufang/miyun/pg1rco11/',
        'https://bj.lianjia.com/zufang/yanqing/pg1rco11/',
        ]

    def parse(self, response):
        # crawl
        houses = response.css('.content__list--item')
        for house in houses:
            item = RentItem()
            item['link'] = house.css('a::attr(href)').get()
            item['title'] = house.css('a::attr(title)').get()
            item['photo'] = house.css('a').css('img::attr(data-src)').get() # 懒加载的真实图片链接不在src
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