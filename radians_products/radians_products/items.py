# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RadiansProductsItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Sku = scrapy.Field()
    Description = scrapy.Field()
    Variations = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()
    Features = scrapy.Field()
    Specs = scrapy.Field()
    Warning = scrapy.Field()
    Keywords = scrapy.Field()
    Parent_sku = scrapy.Field()

    file_urls = scrapy.Field()
    files = scrapy.Field

