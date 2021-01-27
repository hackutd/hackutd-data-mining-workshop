cd %~dp0%output\products
del *.csv
cd %~dp0%output\reviews
del *.csv
cd %~dp0
scrapy crawl product