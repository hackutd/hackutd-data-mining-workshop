from os import name
from amazon_scraping.items import ProductBlacklistItem, ProductInfoItem, ProductReviewDoneItem, ProductReviewItem, StoreInfoItem, StorePageItem
from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response
from sqlite3 import connect
from bs4 import BeautifulSoup, Tag
import re
from amazon_scraping.pipelines import CommitSqlPipeline
from sqlalchemy import table


class ProductReviewSpider(BaseSpider):
	name = 'product_review'

	def start_requests(self):
		"""
		Generates start requests from urls in the product_link table
		"""
		query = '''
		SELECT asin
		FROM product_info
		WHERE (asin NOT IN (
			SELECT asin FROM product_review_done
		))
		'''

		db = connect(self.DB)
		data = db.execute(query).fetchall()
		db.close()

		asins = [data[i][0] for i in range(0, len(data))]
		urls = [f'{self.BASE_URL}/product-reviews/{asins[i]}' for i in range(0, len(data))]

		return [Request(url=urls[i], callback=self.parse_start_url, cb_kwargs=dict(asin=asins[i], depth=0))
				for i in range(0, len(data))]

	def parse_start_url(self, response: Response, asin, depth):
		soup = BeautifulSoup(markup=response.text, features='lxml')
		try:
			reviews = soup.find_all(attrs={'data-hook': 'review'})
			for review in reviews:
				try:
					root_tag: Tag = review
					
					stars_tag: Tag = root_tag.find(attrs={'data-hook': 'review-star-rating'})
					stars_text = stars_tag.get_text().strip()
					stars_match: re.Match = re.search(r'(?P<stars>([0-9.]+)) out of ([0-9.]+)', stars_text)
					stars = int(float(stars_match.group('stars')))
					
					title_tag: Tag = root_tag.find(attrs={'data-hook': 'review-title'})
					title = title_tag.get_text().strip()

					description_tag: Tag = root_tag.find(attrs={'data-hook': 'review-body'})
					description = description_tag.get_text().strip()

					yield ProductReviewItem(asin=asin, stars=stars, title=title, description=description)
				except:
					continue
			if ((reviews) and (depth < 50)):
				pagination = soup.select_one('ul.a-pagination')
				next = pagination.select_one('li.a-last')
				link = next.select_one('a')
				url = self.BASE_URL + link.get('href')
				yield Request(url=url, callback=self.parse_start_url, cb_kwargs=dict(asin=asin, depth=(depth+1)))
			else:
				raise Exception
		except:
			print('Last page reached')
			yield ProductReviewDoneItem(asin=asin)
