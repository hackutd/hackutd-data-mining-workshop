# Import custom-defined ProductItem and ReviewItem types
from amazon_scraping.items import ProductItem, ReviewItem

# Import Spider base class from scrapy
from scrapy import Spider

# Import HTTP Request provided by scrapy
from scrapy.http import Request

# Import BeautifulSoup scraping library
from bs4 import BeautifulSoup


# ProductSpider crawls through multiple search
# result pages to find products. It then yields
# basic information about the products from the product
# overview pages. Also, crawls through multiple
# product review pages to extract and yield reviews.


class ProductSpider(Spider):

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

	# Generates search URL for a given keyword and page number
	def search_url(
			self,
			key,  # Search Keyword
			page_no  # Page number
	):
		# TODO (10) Define search URL format
		pass

	# Generates product overview URL for a given asin
	def overview_url(
			self,
			key		# Product asin
	):
		# TODO (11) Define product overview URL format
		pass

	# Generates product reviews URL for a given asin and page number
	def reviews_url(
			self,
			key,  # Product asin
			page_no  # Page number
	):
		# TODO (12) Define product reviews URL format
		pass

	# Scrapy calls this function at the beginning of the crawl
	def start_requests(self):
		# TODO (13) Yield a search request for each search keyword
		pass

	# Parser for search pages.
	# Yields a product overview and a product review request
	# for each product found in the search page.
	def parse_search(
			self,
			response,  # Scrapy auto-passes the HTML code to 2nd arg
			keyword,  # Search Keyword
			page_no		# Page Number
	):
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# TODO (14) Find all search result items in soup

		# TODO (15) Yield requests for each item found
		#	TODO (15.1) Extract asin from item
		#	TODO (15.2) Yield requests if asin is found
		#		TODO (15.2.1) Yield product overview request
		#		TODO (15.2.2) Yield first product review request

		# TODO (16) Yield request for next page
		# Check if this page had some items
		#	TODO (16.1) Set next page number
		#	TODO (16.2) Check if next page number is within limit
		#		TODO (16.2.1) Recursively yield a request to next page

	# Parser for product overview pages.
	# Extracts attributes of a ProductItem from the response page
	# and yields the item.
	def parse_overview(self, response, asin, keyword):
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# TODO (17.1) Extract and clean product price

		# TODO (17.2) Extract and clean average number of stars

		# TODO (17.3) Extract and clean product name

		# TODO (17.4) Create a ProductItem and yield it

	# Parser for product review pages.
	# Extracts attributes of each ReviewItem from the response page
	# and yields it.
	def parse_reviews(self, response, asin, page_no):
		# Convert response HTML to a beautiful soup for scraping
		soup = BeautifulSoup(markup=response.text, features='lxml')

		# TODO (18) Find all reviews in soup

		# TODO (19) Extract and yield each ReviewItem
		#	TODO (19.1) Extract and clean number of stars
		#	TODO (19.2) Extract and clean review description
		#	TODO (19.3) Create a ReviewItem and yield it

		# TODO (20) Yield request for next page
		# HINT: A repeat of TODO (16), but for Reviews
