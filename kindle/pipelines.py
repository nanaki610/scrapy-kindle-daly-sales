# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CsvPipeline:
    """
    スクレイピングしたアイテムをCSVファイルに保存するパイプラインです。

    このパイプラインは、スパイダーの開始時にCSVファイルを開き、
    記事のタイトル、記事番号、投稿日、URL、本文を含む各アイテムを書き込みます。
    ただし、urlがすでにファイルに存在する場合、アイテムは無視されます。
    """
    def open_spider(self, spider):
        """
        CSVファイルを開き、ヘッダーを書き込みます (新規作成の場合)。
        """
        self.file = open("out.csv", "a+", newline='', encoding='utf-8')
        self.file.seek(0)
        self.existing_urls = set(line.split(',')[3].strip() for line in self.file.readlines())
        
        # 新規作成の場合、ヘッダーを書き込む
        if self.file.tell() == 0:
            self.file.write("title,price,url,image\n")
        
    def close_spider(self, spider):
        """
        CSVファイルを閉じます。
        """
        self.file.close()
        
    def process_item(self, item, spider):
        """
        各アイテムを処理し、CSVファイルに書き込みます。
        ただし、urlがすでにファイルに存在する場合、アイテムは無視されます。
        """
        # 重複チェック
        if item.get('url') in self.existing_urls:
            return item

        # アイテムを書き込む
        line = f"{item.get('title')},{item.get('price')},{item.get('url')},{item.get('image')}\n"
        self.file.write(line)
        self.existing_urls.add(item.get('url'))
        return item
    
