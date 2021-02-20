from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response


class HomeSpider(BaseSpider):
	name = 'home'
	start_urls = [f'{BaseSpider.BASE_URL}/']

	def parse_start_url(self, response: Response):
		yield from self.extract_search_links(response, self.start_urls[0])
		yield from self.extract_product_links(response, self.start_urls[0])
