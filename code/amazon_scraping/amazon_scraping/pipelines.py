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


class CsvPipeline:
	"""
	CsvPipeline is the base class for ProductPipeline and ReviewPipeline.
	It exports all entries that containing the same key to the same
	CSV file, named by its key.
	"""

	def __init__(self, item_type, fields, key_field, out_dir):
		"""
		Class constructor
		:param item_type: Class type of items to export
		:param fields: Array of field names to display
		:param key_field: Field name used for naming files
		:param out_dir: Output sub-directory name
		"""
		# Copy arguments to class attributes
		self.item_type = item_type
		self.fields = fields
		self.key_field = key_field
		self.out_dir = out_dir

	def open_spider(self, spider):
		"""
		Scrapy calls this function when a new spider is opened
		:param spider:  Scrapy auto-passes the spider instance
		"""
		# The exporters dictionary maps file names to CsvItemExporter instances
		self.exporters = {}

	def get_exporter(self, item):
		"""
		Finds / creates an exporter for a given item
		Takes item as an argument and returns an exporter
		:param item: Pass an item to get its exporter
		"""
		#  Extract key from item using ItemAdapter
		adapter = ItemAdapter(item=item)
		key = adapter[self.key_field]

		# Create an exporter for the key, if needed
		# Check if the key doesn't exist in the dictionary
		if (not (key in self.exporters)):
			# Open a CSV file to create a new exporter
			exporter = CsvItemExporter(
				open(file=f'output/{self.out_dir}/{key}.csv', mode='ab'),
				include_headers_line=False
			)

			# Construct the header row from self.fields
			header = {self.fields[i]: self.fields[i]
					  for i in range(0, len(self.fields))}

			# Configure the fields to export
			exporter.fields_to_export = self.fields

			# Start exporting the file
			exporter.start_exporting()

			# Export the header row
			exporter.export_item(item=header)

			# Add exporter to the dictionary
			self.exporters[key] = exporter

		# Return the corresponding exporter
		return self.exporters[key]

	def process_item(self, item, spider):
		"""
		Scrapy calls this function when an item passes through this pipeline
		:param item: Scrapy auto-passes the item instance
		:param spider: Scrapy auto-passes the spider instance
		"""
		# Export matching items
		# Check if the item is an instance of self.item_type
		if isinstance(item, self.item_type):
			# Get the exporter for this item
			exporter = self.get_exporter(item=item)

			# Export the item
			exporter.export_item(item)

		# It's required to return the item after it
		# has been processed by a pipeline
		return item

	def close_spider(self, spider):
		"""
		Scrapy calls this function when a spider is closeed
		:param spider: Scrapy auto-passes the spider instance
		"""
		# For each opened exporter in the dictionary
		for exporter in self.exporters.values():
			# Close the file associated with the exporter
			exporter.finish_exporting()


# Derive ProductPipeline from CsvPipeline


class ProductPipeline(CsvPipeline):
	def __init__(self):
		CsvPipeline.__init__(
			self=self,
			item_type=ProductItem,
			fields=['asin', 'price', 'avg_stars', 'name'],
			key_field='keyword',
			out_dir='products')


# Derive ReviewPipeline from CsvPipeline


class ReviewPipeline(CsvPipeline):
	def __init__(self):
		CsvPipeline.__init__(
			self=self,
			item_type=ReviewItem,
			fields=['stars', 'description'],
			key_field='asin',
			out_dir='reviews')
