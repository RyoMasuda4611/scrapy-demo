import scrapy
from scrapy.loader import ItemLoader
from demo_project.items import QuoteItem

class GoodReadsSpider(scrapy.Spider):
    name = "goodreads"

    def start_requests(self):
        urls = ["https://www.goodreads.com/quotes?page=1"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): 
        for quote in response.selector.xpath("//div[@class='quote']"):
            loader= ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('text', ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath('author', ".//span[@class='authorOrTitle']/text()")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']/a/text()")

            yield {
                'text': quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(),
                'author': quote.xpath(".//span[@class='authorOrTitle']/text()").extract_first(),
                'tags': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract(),
            }
        next_page= response.selector.xpath("//a[@class='next_page']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

