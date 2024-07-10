from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.sale import SaleSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
from tweet_kindle import create_tweet

def spider_closed(spider, reason): #スパイダーが終了したときに実行する関数
  create_tweet() # create_tweet関数を実行

# Yahooニュースのスパイダーを実行
process = CrawlerProcess(settings = get_project_settings()) # Scrapyのプロジェクト設定を読み込み
dispatcher.connect(spider_closed, signal=signals.spider_closed) # スパイダーが終了したときに実行する関数を設定

process.crawl(SaleSpider) # SaleSpiderという名前のスパイダーを使用してクローリングプロセスを初期化
process.start() # クローリングプロセスを開始