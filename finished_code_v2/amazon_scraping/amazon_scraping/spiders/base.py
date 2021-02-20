import re
from scrapy.spiders import CrawlSpider
from amazon_scraping.items import ProductLinkItem, SearchLinkItem, StorePageItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from sqlalchemy import create_engine


class BaseSpider(CrawlSpider):
	# Custom constants
	BASE_DOMAIN = 'www.amazon.com'
	BASE_URL = f'https://{BASE_DOMAIN}'
	DB = 'data.db'

	# Scrapy constants
	allowed_domains = [BASE_DOMAIN]

	def __init__(self):
		self.engine = create_engine("sqlite:///data.db")

	def extract_search_links(self, response, source):
		"""
		Yields all search links found on the page
		"""
		extractor = LxmlLinkExtractor(
			allow=r'/s([/?])', allow_domains=self.allowed_domains)
		links = extractor.extract_links(response)
		for link in links:
			url = link.url
			yield SearchLinkItem(url=url, source=source)
			
	def extract_store_links(self, response, store_id):
		"""
		Yields all store links found on the page
		"""
		extractor = LxmlLinkExtractor(
			allow=r'/stores/', allow_domains=self.allowed_domains)
		links = extractor.extract_links(response)
		for link in links:
			url = link.url
			yield StorePageItem(url=url, store_id=store_id)

	def extract_product_links(self, response, source):
		"""
		Yields all product links found on the page
		"""
		extractor = LxmlLinkExtractor(
			allow=r'/dp/', allow_domains=self.allowed_domains)
		links = extractor.extract_links(response)
		for link in links:
			asin = re.search(
				r'/dp/(?P<asin>([A-Z0-9]+))', link.url).group('asin')
			yield ProductLinkItem(asin=asin, source=source)
