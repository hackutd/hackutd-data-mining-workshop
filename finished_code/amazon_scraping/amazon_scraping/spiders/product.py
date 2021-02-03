# Import custom-defined ProductItem and ReviewItem types
from amazon_scraping.items import ProductItem, ReviewItem

# Import Spider base class from scrapy
from scrapy import Spider

# Import HTTP Request provided by scrapy
from scrapy.http import Request

# Import BeautifulSoup scraping library
from bs4 import BeautifulSoup


class ProductSpider(Spider):
	"""
	ProductSpider crawls through multiple search
	result pages to find products. It then yields
	basic information about the products from the product
	overview pages. Also, crawls through multiple
	product review pages to extract and yield reviews.
	"""

	# Domain name for Base URL
	BASE_DOMAIN = 'amazon.com'

	# Prepended this Base URL to each request
	BASE_URL = f'https://{BASE_DOMAIN}'

	# Array of search keywords
	KEYWORDS = [
		'mechanical+keyboard',
		'mechanical+mouse',
		'gaming+pc'
	]

	# Maximum number of search result pages to crawl
	MAX_SEARCH_PAGES = 3

	# Maximum number of review pages to crawl per product
	MAX_REVIEW_PAGES = 3

	# Spider Name (Scrapy option)
	name = 'product'

	# Array of allowed domain names (Scrapy option)
	allowed_domains = [BASE_DOMAIN]

	def search_url(self, key, page_no):
		"""
		Generates search URL for a given keyword and page number
		:param key: Search Keyword
		:param page_no: Page number
		"""
		# (1) Define search URL format
		return f'{self.BASE_URL}/s?k={key}&page={page_no}'

	def overview_url(self, key):
		"""
		Generates product overview URL for a given asin
		:param key: Product asin
		"""
		# (2) Define product overview URL format
		return f'{self.BASE_URL}/dp/{key}'

	def reviews_url(self, key, page_no):
		"""
		Generates product reviews URL for a given asin and page number
		:param key: Product asin
		:param page_no: Page number
		"""
		# (3) Define product reviews URL format
		return f'{self.BASE_URL}/product-reviews/{key}?pageNumber={page_no}'

	def start_requests(self):
		"""
		Scrapy calls this function at the beginning of the crawl
		"""
		# (4) Yield a search request for each search keyword
		for keyword in self.KEYWORDS:
			yield Request(
				url=self.search_url(key=keyword, page_no=1),
				callback=self.parse_search,
				cb_kwargs=dict(
					keyword=keyword,
					page_no=1))

	def parse_search(self, response, keyword, page_no):
		"""
		Parser for search pages.
		Yields a product overview and a product review request
		for each product found in the search page.
		:param response: Scrapy auto-passes the HTML code
		:param keyword: Search Keyword
		:param page_no: Page Number
		"""
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# (5) Find all search result items in soup
		items = soup.find_all(attrs={'data-component-type': 's-search-result'})

		# (6) Yield requests for each item found
		#	(6.1) Extract asin from item
		#	(6.2) Yield requests if asin is found
		#		(6.2.1) Yield product overview request
		#		(6.2.2) Yield first product review request
		for item in items:
			asin = item.get(key='data-asin')
			if asin:
				yield Request(
					url=self.overview_url(key=asin),
					callback=self.parse_overview,
					cb_kwargs=dict(
						asin=asin,
						keyword=keyword))
				yield Request(
					url=self.reviews_url(key=asin, page_no=1),
					callback=self.parse_reviews,
					cb_kwargs=dict(
						asin=asin,
						page_no=1))

		# (7) Yield request for next page
		# Check if this page had some items
		#	(7.1) Set next page number
		#	(7.2) Check if next page number is within limit
		#		(7.2.1) Recursively yield a request to next page
		if items:
			next_page_no = page_no+1
			if next_page_no <= self.MAX_SEARCH_PAGES:
				yield Request(
					url=self.search_url(key=keyword, page_no=next_page_no),
					callback=self.parse_search,
					cb_kwargs=dict(
						keyword=keyword,
						page_no=next_page_no))

	def parse_overview(self, response, asin, keyword):
		"""
		Parser for product overview pages.
		Extracts attributes of a ProductItem from the response page
		and yields the item.
		:param response: Scrapy auto-passes the HTML code
		:param asin: Product asin
		:param keyword: Search Keyword
		"""
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# (8.1) Extract and clean product price
		price = soup.find(
			attrs={'data-feature-name': 'priceInsideBuyBox'}).get_text().strip()
		price = price[1:]

		# (8.2) Extract and clean average number of stars
		avg_stars = soup.find(
			attrs={'data-hook': 'rating-out-of-text'}).get_text().strip()
		avg_stars = avg_stars.split()[0]

		# (8.3) Extract and clean product name
		name = soup.find(
			attrs={'data-feature-name': 'title'}).get_text().strip()

		# (8.4) Create a ProductItem and yield it
		yield ProductItem(keyword=keyword, asin=asin, price=price,
						  avg_stars=avg_stars, name=name)

	def parse_reviews(self, response, asin, page_no):
		"""
		Parser for product review pages.
		Extracts attributes of each ReviewItem from the response page
		and yields it.
		:param response: Scrapy auto-passes the HTML code
		:param asin: Product asin
		:param page_no: Page Number
		"""
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# (9) Find all reviews in soup
		reviews = soup.find_all(attrs={'data-hook': 'review'})

		# (10) Extract and yield each ReviewItem
		#	(10.1) Extract and clean number of stars
		#	(10.2) Extract and clean review description
		#	(10.3) Create a ReviewItem and yield it

		for review in reviews:
			stars = review.find(
				attrs={'data-hook': 'review-star-rating'}).get_text().strip()
			stars = stars.split()[0]

			description = review.find(
				attrs={'data-hook': 'review-body'}).get_text().strip()

			yield ReviewItem(asin=asin, stars=stars,
							 description=description)

		# (11) Yield request for next page
		# HINT: A repeat of TASK (7), but for Reviews
		if reviews:
			next_page_no = page_no+1
			if next_page_no <= self.MAX_REVIEW_PAGES:
				yield Request(
					url=self.reviews_url(key=asin, page_no=next_page_no),
					callback=self.parse_reviews,
					cb_kwargs=dict(
						asin=asin,
						page_no=next_page_no))