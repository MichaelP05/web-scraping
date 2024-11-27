import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                "text": quote.css("span.text::text").get().strip('“”'),
                "author": quote.css("span small.author::text").get(),
            }
if __name__ == '__main__':
    
    url = "https://www.bbc.com/sport"
    user_agent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"