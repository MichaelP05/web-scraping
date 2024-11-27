import scrapy

class AuthorTSpider(scrapy.Spider):
    name = "author_t"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/", "https://quotes.toscrape.com/page/2/" ]

    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                "quote": quote.css("span.text::text").get().strip('“”'),
                "author": quote.css("span small.author::text").get(),
            }



class QuotesSpider(scrapy.Spider):
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        elements = response.xpath("//small[@class='author']/text()").getall()
        for element in elements:
            yield {
                'author': element
            }
