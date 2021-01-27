# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface


# Import ItemAdapter to extract item key
from itemadapter import ItemAdapter

# Import custom-defined ProductItem and ReviewItem types
from amazon_scraping.items import ProductItem, ReviewItem

# Import CsvItemExporter provided by scrapy
from scrapy.exporters import CsvItemExporter


# AmazonPipeline is the base class for ProductPipeline and ReviewPipeline.
# It exports all entries that containing the same key to the same
# CSV file, named by its key.


class AmazonPipeline:

	# Class constructor
	def __init__(
		self,		# Python auto-passes 'this' object to 1st arg
		item_type,  # Pass the class type of objects
		fields, 	# Pass an array of field (column) names to display
		key_field, 	# Pass the field name you want to use for filenames
		out_dir		# Pass the output sub-directory name
	):
		# Copy arguments to class attributes
		self.item_type = item_type
		self.fields = fields
		self.key_field = key_field
		self.out_dir = out_dir

	# Scrapy calls this function when a new spider is opened
	def open_spider(
		self,
		spider  # Scrapy auto-passes the spider instance to 2nd arg
	):
		# TODO (3) Initialize a dictionary of exporters
		# Maps file names to CsvItemExporter instances
		pass

	# Finds / creates an exporter for a given item
	# Takes item as an argument and returns an exporter
	def get_exporter(
		self,
		item  # Pass an item to get its exporter
	):
		# TODO (4) Extract key from item using ItemAdapter

		# TODO (5) Create an exporter for the key, if needed
		# Check if the key doesn't exist in the dictionary

		#	TODO (5.1) Open a CSV file to create a new exporter

		#	TODO (5.2) Construct the header row from self.fields

		#	TODO (5.3) Configure the fields_to_export

		#	TODO (5.4) Call the start_exporting function

		#	TODO (5.5) Export the header row

		#	TODO (5.6) Add exporter to the dictionary

		# TODO (6) Return the corresponding exporter
		pass

	# Scrapy calls this function when an item passes through this pipeline
	def process_item(
		self,
		item,  # Scrapy auto-passes the item instance to 2nd arg
		spider  # Scrapy auto-passes the spider instance to 3rd arg
	):
		# TODO (7) Export matching items
		# Check if the item is an instance of self.item_type

		#	TODO (7.1) Get the exporter for this item

		#	TODO (7.2) Export the item

		# It's required to return the item after it
		# has been processed by a pipeline
		return item

	# Scrapy calls this function when a spider is closeed
	def close_spider(
		self,
		spider  # Scrapy auto-passes the spider instance to 2nd arg
	):
		# TODO (8) Close all opened exporters in the dictionary
		# Call the finish_exporting function for each exporter

		pass


# Derive ProductPipeline from AmazonPipeline


class ProductPipeline(AmazonPipeline):
	def __init__(self):
		AmazonPipeline.__init__(
			self=self,
			item_type=ProductItem,
			fields=['asin', 'price', 'avg_stars', 'name'],
			key_field='keyword',
			out_dir='products')


# Derive ReviewPipeline from AmazonPipeline


class ReviewPipeline(AmazonPipeline):
	def __init__(self):
		AmazonPipeline.__init__(
			self=self,
			item_type=ReviewItem,
			fields=['stars', 'description'],
			key_field='asin',
			out_dir='reviews')
