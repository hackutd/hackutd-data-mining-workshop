# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html


# Import Item and Field types from scrapy
from scrapy import Item, Field


# Define ProductItem class attributes
class ProductItem(Item):
	asin = Field()
	price = Field()
	avg_stars = Field()
	name = Field()
	keyword = Field()


# Define ReviewItem class attributes
class ReviewItem(Item):
	stars = Field()
	description = Field()
	asin = Field()
