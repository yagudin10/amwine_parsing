# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field()
    brand = scrapy.Field()
    section = scrapy.Field()
    price_data = scrapy.Field()
    stock = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
    variants = scrapy.Field()

class PriceItem(scrapy.Item):
    current = scrapy.Field()
    original = scrapy.Field()
    sale_tag = scrapy.Field()

class StockItem(scrapy.Item):
    in_stock = scrapy.Field()
    count = scrapy.Field()

class AssetsItem(scrapy.Item):
    main_image = scrapy.Field()
    set_images = scrapy.Field()
    view360 = scrapy.Field()
    video = scrapy.Field()

class MetadataItems(scrapy.Item):
    __description = scrapy.Field()
    article = scrapy.Field()
    producer = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    alco = scrapy.Field()
    temperature = scrapy.Field()


