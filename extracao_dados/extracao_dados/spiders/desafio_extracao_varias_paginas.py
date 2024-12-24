import scrapy

class QuotesToScrapeSpider(scrapy.Spider):
    # Identidade
    name = 'varrer_paginas'
    # Request

    def start_requests(self):
        # Definir url(s) a varrer
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        # Vamos extrair o Texto, autor e as tags do site para um arquivo
        for elemento in response.xpath('//div[@class="quotes"]/div[@class="quote"]'):
            yield {
                'frase': elemento.xpath('.//div[@class="quoteText"]/text()').get(),
                'autor': elemento.xpath('.//div[@class="quoteText"]/span[@class="authorOrTitle"]/text()').get(),
                'tags': elemento.xpath('.//div[@class="greyText smallText left"]/a/text()').getall()
            }
        # Varrendo todas as páginas
        try: 
            link_proxima_pagina = response.xpath('//a[@class="next_page"]/@href').get()
            if link_proxima_pagina is not None:
                proxima_pagina_url_completo = response.urljoin(link_proxima_pagina)
                yield scrapy.Request(url=proxima_pagina_url_completo, callback=self.parse)
         
        except:
            print('Chegamos na última página')