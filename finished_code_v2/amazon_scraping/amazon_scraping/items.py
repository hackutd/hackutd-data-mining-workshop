# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html


from scrapy_sqlitem import SqlItem
from scrapy_sqlitem.sqlitem import SqlAlchemyItemMeta
from sqlalchemy import Table, MetaData, Column, String, Integer, Numeric, UniqueConstraint
from sqlalchemy.sql.schema import ForeignKey


class ProductBlacklistItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'product_blacklist',
        MetaData(),
        Column('asin', String, ForeignKey('product_link.asin'),
               nullable=False, unique=True, primary_key=True,),
    )


class ProductInfoItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'product_info',
        MetaData(),
        Column('asin', String, ForeignKey('product_link.asin'),
               nullable=False, unique=True, primary_key=True,),
        Column('name', String),
        Column('price', Numeric),
        Column('avg_stars', Numeric),
        Column('store_id', Integer, ForeignKey('store_info.id')),
        Column('store_name', String),
        Column('store_root_url', String),
    )


class ProductLinkItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'product_link',
        MetaData(),
        Column('asin', String, nullable=False,
               unique=True, primary_key=True),
        Column('source', String, nullable=False),
    )


class ProductReviewItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'product_review',
        MetaData(),
        Column('id', Integer, nullable=False,  unique=True,
               primary_key=True, autoincrement=True),
        Column('asin', String, ForeignKey(
            'product_link.asin'), nullable=False),
        Column('stars', Integer),
        Column('title', String),
        Column('description', String),
        UniqueConstraint('stars', 'description', 'asin', 'title'),
    )


class ProductReviewDoneItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'product_review_done',
        MetaData(),
        Column('asin', String, ForeignKey('product_link.asin'),
               nullable=False,  unique=True, primary_key=True),
    )


class SearchLinkItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'search_link',
        MetaData(),
        Column('url', String, nullable=False,
               unique=True, primary_key=True),
        Column('source', String, nullable=False),
    )


class StoreInfoItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'store_info',
        MetaData(),
        Column('id', Integer, nullable=False,
               unique=True, primary_key=True, autoincrement=True),
        Column('name', String, nullable=False, unique=True),
        Column('root_url', String, nullable=False, unique=True),
    )


class StorePageItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table(
        'store_page',
        MetaData(),
        Column('url', String,  nullable=False,
               unique=True, primary_key=True),
        Column('store_id', Integer, ForeignKey(
            'store_info.id'), nullable=False),
    )
