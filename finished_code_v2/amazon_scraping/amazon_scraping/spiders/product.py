from os import name
from amazon_scraping.items import ProductBlacklistItem, ProductInfoItem, StoreInfoItem, StorePageItem
from amazon_scraping.spiders.base import BaseSpider
from scrapy.http import Request, Response
from sqlite3 import connect
from bs4 import BeautifulSoup, Tag
import re
from amazon_scraping.pipelines import CommitSqlPipeline
from sqlalchemy import table


class ProductSpider(BaseSpider):
	name = 'product'

	def start_requests(self):
		"""
		Generates start requests from urls in the product_link table
		"""
		query = '''
		SELECT asin
		FROM product_link
		WHERE asin NOT IN
		(
			SELECT asin
			FROM product_info
			UNION
			SELECT asin
			FROM product_blacklist
		)
		'''

		db = connect(self.DB)
		data = db.execute(query).fetchall()
		db.close()

		asins = [data[i][0] for i in range(0, len(data))]
		urls = [f'{self.BASE_URL}/dp/{asins[i]}' for i in range(0, len(data))]

		return [Request(url=urls[i], callback=self.parse_start_url, cb_kwargs=dict(asin=asins[i]))
				for i in range(0, len(data))]

	def parse_start_url(self, response: Response, asin):
		soup = BeautifulSoup(markup=response.text, features='lxml')
		try:
			name_tag: Tag = soup.select_one('h1#title')
			name = name_tag.get_text().strip()
		except:
			name = None
		price_tags: Tag = soup.select(
			'[data-feature-name="priceInsideBuyBox"], #newBuyBoxPrice, #priceblock_dealprice, #priceblock_ourprice')
		price = None
		for price_tag in price_tags:
			try:
				price_text = price_tag.get_text().strip()
				price_match: re.Match = re.search(
					r'\$(?P<price>([0-9.]+))', price_text)
				price = float(price_match.group('price'))
				break
			except:
				continue
		try:
			avg_stars_tag: Tag = soup.find(
				attrs={'data-hook': 'rating-out-of-text'})
			avg_stars_text = avg_stars_tag.get_text().strip()
			avg_stars_match: re.Match = re.search(
				r'(?P<avg_stars>([0-9.]+)) out of ([0-9.]+)', avg_stars_text)
			avg_stars = float(avg_stars_match.group('avg_stars'))
		except:
			avg_stars = None
		try:
			store_div_tag: Tag = soup.find(
				attrs={'data-feature-name': 'bylineInfo'})
			store_tag: Tag = store_div_tag.select_one('a.a-link-normal')
			try:
				store_name_text = store_tag.get_text().strip()
				store_name_match: re.Match = re.search(r'(Brand: (?P<n1>(.+)))|(Visit ((the )?)(?P<n2>(.+))( Store| Page))', store_name_text)
				store_name = store_name_match.group('n1')
				if store_name is None:
					store_name = store_name_match.group('n2')
			except:
				store_name = None
			try:
				store_root_url = self.BASE_URL + store_tag.get('href')
			except:
				store_root_url = None
		except:
			store_name = None
			store_root_url = None

		if ((price is None) or (avg_stars is None) or (store_name is None) or (store_root_url is None)):
			yield ProductBlacklistItem(asin=asin)
		else:
			yield StoreInfoItem(name=store_name, root_url=store_root_url)
			
			item = StoreInfoItem()
			item.table.metadata.bind = self.engine
			row = item.table.select().where(item.table.c.name == store_name).execute().fetchone()
			store_id = row[0]

			yield StorePageItem(url=store_root_url, store_id=store_id)
			yield ProductInfoItem(asin=asin, name=name, price=price, avg_stars=avg_stars, store_id=store_id)
