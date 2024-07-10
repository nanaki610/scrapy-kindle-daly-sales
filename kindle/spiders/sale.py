import os
import sys
import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader

# 現在のファイルのディレクトリパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# 親ディレクトリをsys.pathに追加
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
from items import KindleItem

class SaleSpider(scrapy.Spider):
    name = 'sale'
    
    def start_requests(self):
        yield scrapy.Request(
            'https://www.amazon.co.jp/kindle-dbs/browse?widgetId=ebooks-deals-storefront_KindleDailyDealsStrategy&sourceType=recs',
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'encoding': 'utf-8', # Add this line to fix the encoding issue
                'playwright_page_methods': [
                    PageMethod("screenshot", path="example.png", full_page=True),
                    PageMethod('wait_for_selector', 'div#browse-grid-view'),
                ]
            }
        )
        
    def get_title(self, title):
        if title:
            return title.strip()
        return title
    def get_price(self, price):
        if price:
            return int(price.replace('￥', '').replace(',', '').strip())
        return 0
    def get_url(self, url):
        base_url = 'https://www.amazon.co.jp'
        if url:
            return base_url + (url.split('?')[0] if '?' in url else url)
        return url

    def parse(self, response):
        products = response.css('div.a-section.browse-grid-view-item-unit')
        
        for product in products:
            title = self.get_title(product.css('span span[aria-hidden="true"]:nth-of-type(1)::text').get()),
            price = self.get_price(product.css('span.a-list-item.a-size-small.a-color-secondary span[class*="price"]::text').get()),
            url = self.get_url(product.css('div#sponsoredLabel-title a.a-link-normal::attr(href)').get()),
            image = product.css('a[class="a-link-normal browse-grid-view-link"] img::attr(src)').get(),
            
            # ItemLoaderを使ってデータを格納
            loader = ItemLoader(item=KindleItem(), response=response)
            loader.add_value('title', title)
            loader.add_value('price', price)
            loader.add_value('url', url)
            loader.add_value('image', image)
            yield loader.load_item()
