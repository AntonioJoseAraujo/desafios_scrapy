# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join

def tirar_espaco_em_branco(valor):
    return valor.strip() 


def remover_aspas(valor):
    return valor.replace(u"\u2019", '')


def maiusculo(valor):
    return valor.upper()


class CorrecaoItem(scrapy.Item):
    frase = scrapy.Field(
      
        input_processor=MapCompose(tirar_espaco_em_branco, remover_aspas),
        output_processor=TakeFirst()  
    )
    autor = scrapy.Field(
        input_processor=MapCompose(tirar_espaco_em_branco, maiusculo),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        output_processor=Join(';')
    )

