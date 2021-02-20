from amazon_scraping.items import SearchLinkItem
from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response
from sqlite3 import connect
from bs4 import BeautifulSoup


class SearchSpider(BaseSpider):
	name = 'search'

	def start_requests(self):
		"""
		Generates start requests from urls in the search_link table
		"""
		query = 'SELECT url FROM search_link'

		db = connect(self.DB)
		data = db.execute(query).fetchall()
		db.close()

		urls = [data[i][0] for i in range(0, len(data))]

		return [Request(url=urls[i])
				for i in range(0, len(data))]

	def parse_start_url(self, response: Response):
		request: Request = response

		# Extract all Product links from this page
		yield from self.extract_product_links(response, request.url)

		# Try to Request the Next page
		try:
			soup = BeautifulSoup(markup=response.text, features='lxml')
			pagination = soup.select_one('ul.a-pagination')
			next = pagination.select_one('li.a-last')
			link = next.select_one('a')
			url = self.BASE_URL + link.get('href')
			yield Request(url=url, callback=self.parse_start_url)
		except:
			print('Last page reached')