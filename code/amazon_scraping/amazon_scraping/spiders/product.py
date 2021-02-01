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
		# TODO (1) Define search URL format
		pass

	def overview_url(self, key):
		"""
		Generates product overview URL for a given asin
		:param key: Product asin
		"""
		# TODO (2) Define product overview URL format
		pass

	#
	def reviews_url(self, key, page_no):
		"""
		Generates product reviews URL for a given asin and page number
		:param key: Product asin
		:param page_no: Page number
		"""
		# TODO (3) Define product reviews URL format
		pass

	def start_requests(self):
		"""
		Scrapy calls this function at the beginning of the crawl
		"""
		# TODO (4) Yield a search request for each search keyword
		pass

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

		# TODO (5) Find all search result items in soup

		# TODO (6) Yield requests for each item found
		#	TODO (6.1) Extract asin from item
		#	TODO (6.2) Yield requests if asin is found
		#		TODO (6.2.1) Yield product overview request
		#		TODO (6.2.2) Yield first product review request

		# TODO (7) Yield request for next page
		# Check if this page had some items
		#	TODO (7.1) Set next page number
		#	TODO (7.2) Check if next page number is within limit
		#		TODO (7.2.1) Recursively yield a request to next page

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

		# TODO (8.1) Extract and clean product price

		# TODO (8.2) Extract and clean average number of stars

		# TODO (8.3) Extract and clean product name

		# TODO (8.4) Create a ProductItem and yield it

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

		# TODO (9) Find all reviews in soup

		# TODO (10) Extract and yield each ReviewItem
		#	TODO (10.1) Extract and clean number of stars
		#	TODO (10.2) Extract and clean review description
		#	TODO (10.3) Create a ReviewItem and yield it

		# TODO (11) Yield request for next page
		# HINT: A repeat of TODO (7), but for Reviews
