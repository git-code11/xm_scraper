# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XmRunItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    vtype = scrapy.Field()
    year = scrapy.Field()
    duration= scrapy.Field()
    genre= scrapy.Field()
    country= scrapy.Field()
    name = scrapy.Field()
    x_id = scrapy.Field()
    tmdb_id = scrapy.Field()
    movie_url = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    similar = scrapy.Field()


