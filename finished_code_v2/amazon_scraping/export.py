from scrapy import Field
from scrapy.exporters import CsvItemExporter
from sqlite3 import connect

DB = 'data.db'
db = connect(DB)


def get_stores():
	query = '''
	SELECT store_id
	FROM product_info
	GROUP BY store_id
	'''
	data = db.execute(query).fetchall()
	ids = [data[i][0] for i in range(0, len(data))]
	return (data, ids)


def get_products(store_id):
	query = '''
	SELECT product_info.asin, product_info.name, product_info.price, product_info.avg_stars, product_info.store_id, store_info.name AS store_name
	FROM product_info, store_info
	WHERE (
		(product_info.store_id  = store_info.id)
		AND (product_info.store_id = ?)
	)
	'''
	params = (store_id, )
	data = db.execute(query, params).fetchall()
	asins = [data[i][0] for i in range(0, len(data))]
	return (data, asins)


def get_reviews(asin):
	query = '''
	SELECT product_review.asin, product_review.stars, product_review.title, product_review.description
	FROM product_review
	WHERE (asin = ?)
	'''
	params = (asin, )
	data = db.execute(query, params).fetchall()
	return data


def export(exporter, data, header):
	exporter.start_exporting()
	exporter.csv_writer.writerow(header)
	exporter.csv_writer.writerows(data)
	exporter.finish_exporting()


def export_products(store_id, data):
	exporter = CsvItemExporter(
		file=open(f'output/products/{store_id}.csv', 'wb'), include_headers_line=False)
	header = ('asin', 'name', 'price', 'avg_stars', 'store_id', 'store_name', )
	export(exporter=exporter, data=data, header=header)


def export_reviews(asin, data):
	exporter = CsvItemExporter(
		file=open(f'output/reviews/{asin}.csv', 'wb'), include_headers_line=False)
	header = ('asin', 'stars', 'title', 'description', )
	export(exporter=exporter, data=data, header=header)


(store_data, store_ids) = get_stores()
for store_id in store_ids:
	(product_data, product_asins) = get_products(store_id=store_id)
	if product_data:
		export_products(store_id=store_id, data=product_data)
		for product_asin in product_asins:
			review_data = get_reviews(asin=product_asin)
			if review_data:
				export_reviews(asin=product_asin, data=review_data)


db.close()
