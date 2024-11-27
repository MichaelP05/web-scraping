# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter


class FirstScrapyPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("quotes.db")
        self.cursor = self.connection.cursor()
        sql = """
            create table if not exists quotes (
                author text,
                quote text
            )
        """
        self.cursor.execute(sql)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            "insert into quotes (author, quote) values (?, ?)",
            (item['author'], item['quote'])
        )
        self.connection.commit()
        return item
