from amazon_scraping.items import ProductLinkItem, SearchLinkItem
import re
from sqlite3 import connect
from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response


class StorePagesSpider(BaseSpider):
	name = 'store_pages'

	def start_requests(self):
		query = '''
		SELECT url, store_id from store_page
		'''

		db = connect(self.DB)
		data = db.execute(query).fetchall()
		db.close()

		urls = [data[i][0] for i in range(0, len(data))]
		store_ids = [data[i][1] for i in range(0, len(data))]

		return [Request(urls[i], callback=self.parse_start_url, cb_kwargs=dict(store_id=store_ids[i]))
				for i in range(0, len(data))]

	def parse_start_url(self, response: Response, store_id):
		request: Request = response.request
		yield from self.extract_product_links(response=response, source=request.url)
		yield from self.extract_store_links(response=response, store_id=store_id)
