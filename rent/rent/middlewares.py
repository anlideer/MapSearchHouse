# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
import time
import requests

proxies = {}
expire_time = 0
get_ip_api = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

class RentSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RentDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents
 
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist("USER_AGENTS"))
 
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleWare(object):  
    def process_request(self,request, spider):  
        '''对request对象加上proxy'''  
        proxy = self.get_proxy()  
        print("this is request ip:"+proxy)  
        request.meta['proxy'] = proxy   
 
    def process_response(self, request, response, spider):  
        # 如果返回的response状态不是200，重新生成当前request对象  
        if response.status != 200:
            self.switch_ip()    # 手动换ip（可能这个ip过快了）
            proxy = self.get_proxy()  
            print("this is response ip:"+proxy)  
            # 对当前reque加上代理  
            request.meta['proxy'] = proxy   
            return request  
        return response
    
    def get_proxy(self):  
        global expire_time
        global proxies
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 20))   # leave 20s for scrapy
        if current_time > str(expire_time):
            self.switch_ip()
        return proxies
    
    def switch_ip(self):
        global get_ip_api
        global expire_time
        global proxies
        res = requests.get(get_ip_api)
        proxyHost = res.json()['data'][0]['ip']
        proxyPort = res.json()['data'][0]['port']
        expire_time = res.json()['data'][0]['expire_time']
        http_pro = "http://" + str(proxyHost) + ":" + str(proxyPort)
        #https_pro = "https://" + str(proxyHost) + ":" + str(proxyPort)
        # proxies = {
        #     "http" : http_pro,
        #     "https": https_pro
        # }
        proxies = http_pro
