# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
from .useragent import agents
from redis import Redis
from scrapy.utils.log import logger
class CdhouseSpiderMiddleware(object):
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

		# Must return an iterable of Request, dict or Item objects.
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Request, dict
		# or Item objects.
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


class IgnoreRequest(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return f"{self.message}"


# 在中间件中执行url重复过滤，有效提高性能
class SingleDownloadMiddleware(object):
	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls(crawler.settings,crawler)
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s
	
	# 用redis执行，这里的参数都
	# 是从from_crawler传来的
	def __init__(self,setting,crawler):
		super(SingleDownloadMiddleware, self).__init__()
		self.conn = Redis(host=setting['REDIS_URL'], port=setting['REDIS_PORT'])

	def process_request(self, request, spider):
		req_url = request.url
		
		if self.conn.sismember('already_url', req_url):
			# 抛出自定义错误.
			# raise IgnoreRequest("IgnoreRequest :%s" % req_url)
			spider.logger.info("IgnoreRequest {}".format(req_url))
		else:
			self.conn.sadd('already_url', req_url)
			return None
			
	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)

	def process_exception(self, request, exception, spider):
		print("cuowu",type(exception))
		return None


# 设置随机浏览器代理
class UserAgentmiddleware(UserAgentMiddleware):
	# 当每个request通过下载中间件时，调用该方法； 返回None，request，response，或raise ignoreRequest
	def process_request(self, request, spider):
		agent = random.choice(agents)
		request.headers.setdefault(b'User-Agent', agent)
		if request.url.startswith("https://cd.zu.fang.com/"):
			request.headers.setdefault("Referer", "https://cd.zu.fang.com/")
		elif request.url.startswith("https://cd.esf.fang.com/"):
			request.headers.setdefault("Referer","https://cd.esf.fang.com/")
		elif request.url.startswith("https://cd.newhouse.fang.com/house/s/"):
			request.headers.setdefault("Referer","https://cd.newhouse.fang.com/house/s/")

		if "search" in request.url:
			raise IgnoreRequest("found ignorerequest")
		# 切换ip代理
		# request.headers.setdefault(
		# 	'authorization', 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20')
		# FIXME:修改成房天下的host
		# request.headers.setdefault("Host", "www.zhihu.com")
