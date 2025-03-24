import scrapy
# CamelCase


class QuotesToScrapeSpider(scrapy.Spider):
    # Identidade
    name = 'extra_dados'
    # Request

    def start_requests(self):
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        for elemento in response.xpath('//div[@class="quotes"]/div[@class="quote"]'):
            yield {
                'frase': elemento.xpath('.//div[@class="quoteText"]/text()').get(),
                'autor': elemento.xpath('.//div[@class="quoteText"]/span[@class="authorOrTitle"]/text()').get(),
                'tags': elemento.xpath('.//div[@class="greyText smallText left"]/a/text()').getall()
            }
