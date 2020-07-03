# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SongItem(scrapy.Item):
    artist = scrapy.Field()
    genre = scrapy.Field()
    lyricsBy = scrapy.Field()
    musicBy = scrapy.Field()
    songTitle = scrapy.Field()
    key = scrapy.Field()
    lyrics = scrapy.Field()
    artistName = scrapy.Field()
    movieName = scrapy.Field()
    url = scrapy.Field()
    pass
