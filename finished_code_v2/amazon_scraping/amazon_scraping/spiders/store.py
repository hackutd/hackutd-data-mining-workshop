from amazon_scraping.items import ProductLinkItem, SearchLinkItem
import re
from sqlite3 import connect
from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response


class StoreSpider(BaseSpider):
	name = 'store'

	def start_requests(self):
		query = '''
		SELECT store_info.id, store_info.root_url, product_info.asin
		FROM store_info, product_info
		WHERE (store_info.id = product_info.store_id)
		'''

		db = connect(self.DB)
		data = db.execute(query).fetchall()
		db.close()

		ids = [data[i][0] for i in range(0, len(data))]
		root_urls = [data[i][1] for i in range(0, len(data))]
		source_asins = [data[i][2] for i in range(0, len(data))]
		sources = [f'{self.BASE_URL}/dp/{source_asins[i]}' for i in range(0, len(data))]

		return [Request(root_urls[i], callback=self.parse_start_url, cb_kwargs=dict(id=ids[i], source=sources[i]))
				for i in range(0, len(data))]

	def parse_start_url(self, response: Response, id, source):
		request: Request = response.request
		url = response.url
		if re.fullmatch(rf'^{self.BASE_URL}/s[/?](.+)', url):
			yield SearchLinkItem(url=url, source=source)
		else:
			if re.fullmatch(rf'^{self.BASE_URL}/stores/(.+)', url):
				yield from self.extract_product_links(response=response, source=request.url)
				yield from self.extract_store_links(response=response, store_id=id)