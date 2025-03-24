'''
# Vamos atualizar a spider do site GoodReads
# 1 - Remover todos os caracteres especiais \u2019 das frases
# 2 - Colocar o nome de todos os autores em MAIÚSCULO
# 3 - Remover os espaços em branco dentro das frases e autores
# 4 - Mudar o separador das tags de uma vírgula, para um ponto e vírgula(;)
'''

import scrapy
from scrapy.loader import ItemLoader
from extracao_dados.items import CorrecaoItem


class QuotesToScrapeSpider(scrapy.Spider):
    # Identidade
    name = 'correcao_dados'
    # Request

    def start_requests(self):
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        for elemento in response.xpath('//div[@class="quotes"]/div[@class="quote"]'):
            loader = ItemLoader(item=CorrecaoItem(), selector=elemento, response=response)
            loader.add_xpath('frase','.//div[@class="quoteText"]/text()')
            loader.add_xpath('autor','.//div[@class="quoteText"]/span[@class="authorOrTitle"]/text()')
            loader.add_xpath('tags','.//div[@class="greyText smallText left"]/a/text()')
            yield loader.load_item()

           # Varrendo todas as páginas
        try: 
            link_proxima_pagina = response.xpath('//a[@class="next_page"]/@href').get()
            if link_proxima_pagina is not None:
                proxima_pagina_url_completo = response.urljoin(link_proxima_pagina)
                yield scrapy.Request(url=proxima_pagina_url_completo, callback=self.parse)
         
        except:
            print('Chegamos na última página')