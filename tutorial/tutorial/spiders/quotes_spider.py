import scrapy
import re
import json
import ast
from datetime import datetime
from tutorial.items import *

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://amwine.ru/catalog/krepkie_napitki/viski/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, cookies = {'AMWINE__shop_id' : '900'}, callback=self.parse_page)

    def parse_page(self, response):
        pattern = re.compile(r"window\.products\s\=\s(\[{.*?}\]);", re.MULTILINE | re.DOTALL)
        data = response.xpath("//script[contains(., 'window.products')]/text()").re(pattern)[0]
        pattern = re.compile(r"window\.catalogProps\s\=\s({.*?});", re.MULTILINE | re.DOTALL)
        pattern = re.compile(r"window\.catalogSectionParams\s\=\s({.*?});", re.MULTILINE | re.DOTALL)
        params = response.xpath("//script[contains(., 'window.catalogSectionParams')]/text()").re(pattern)[0]
        pattern = re.compile(r"window\.catalogSectionAjaxPath\s\=\s\'(.*?)\';", re.MULTILINE | re.DOTALL)
        products_path = response.xpath("//script[contains(., 'window.catalogSectionAjaxPath')]/text()").re(pattern)[0]
        pattern = re.compile(r"window\.productsTotalCount\s\=\s(.*?);", re.MULTILINE | re.DOTALL)
        products_count = response.xpath("//script[contains(., 'window.productsTotalCount')]/text()").re(pattern)[0]
        pattern = re.compile(r"window\.catalogSectionCurrentFilter\s\=\s(.*?);", re.MULTILINE | re.DOTALL)
        current_filter = response.xpath("//script[contains(., 'window.catalogSectionCurrentFilter')]/text()").re(pattern)[0]

        data = json.loads(data.replace("\'", "\""))
        for r in data:
            product = ProductItem()
            price_data = PriceItem()
            stock = StockItem()
            assets = AssetsItem()
            metadata = MetadataItems()
            product['timestamp'] = datetime.timestamp(datetime.now())
            product['RPC'] = r['id']
            product['url'] = 'https://amwine.ru{}'.format(r['link'])
            product['title'] = r['props']['russian_name']
            product['marketing_tags'] = []
            product['brand'] = ''  
            product['section'] = r['category'].split('/')
            stock['in_stock'] = r['available']
            if r['available']:
                price_data['current'] = float(r['price'])
                price_data['original'] = float(r['price'] if 'old_price' not in r.keys() else r['old_price'])
                price_data['sale_tag'] = 'Скидка {0}'.format(r['sale']) if r['sale'] else ''
                stock['count'] = int(r['available_quantity'])
            else:
                price_data['current'] = ''
                price_data['original'] = ''
                price_data['sale_tag'] = ''
                stock['count'] = 0
            assets['main_image'] = 'https://amwine.ru{}'.format(r['preview_picture'])
            product['price_data'] = price_data
            product['stock'] = stock
            product['assets'] = assets
            product['metadata'] = metadata
            product['variants'] = 1
            yield product

        params = json.loads(params.replace("\'", "\""))
        post_data = {}
        post_data['json'] = 'y'
        for key in params.keys():
            post_data['params[' + key + ']'] = params[key]
        post_data['PAGEN_1'] = 2
        current_filter = json.loads(current_filter.replace("\'", "\""))
        for key in current_filter.keys():
            post_data['current_filter[' + key + ']'] = current_filter[key]
        print(post_data)
        yield scrapy.Request(url='https://amwine.ru{}'.format(products_path), 
            method='POST', 
            body=json.dumps(post_data), 
            callback=self.parse_other_pages)

    def parse_other_pages(self, response):
        json_text = json.loads(response.text)
        print(json_text)
        for item in json_text['products']:
            product = ProductItem()
            price_data = PriceItem()
            stock = StockItem()
            assets = AssetsItem()
            metadata = MetadataItems()
            product['timestamp'] = datetime.timestamp(datetime.now())
            product['RPC'] = item['id']
            product['url'] = 'https://amwine.ru{}'.format(item['link'])
            product['title'] = item['props']['russian_name']
            product['marketing_tags'] = []
            product['brand'] = ''  
            product['section'] = item['category'].split('/')
            stock['in_stock'] = item['available']
            if item['available']:
                price_data['current'] = float(item['price'])
                price_data['original'] = float(item['price'] if 'old_price' not in item.keys() else item['old_price'])
                price_data['sale_tag'] = 'Скидка {0}'.format(item['sale']) if item['sale'] else ''
                stock['count'] = int(item['available_quantity'])
            else:
                price_data['current'] = ''
                price_data['original'] = ''
                price_data['sale_tag'] = ''
                stock['count'] = 0
            assets['main_image'] = 'https://amwine.ru{}'.format(item['preview_picture'])
            product['price_data'] = price_data
            product['stock'] = stock
            product['assets'] = assets
            product['metadata'] = metadata
            product['variants'] = 1
            print(product)
            yield product

        

