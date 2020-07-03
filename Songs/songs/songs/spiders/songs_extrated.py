import scrapy
from ..items import SongItem
from datetime import datetime
import re
import os


class Fundrazr(scrapy.Spider):
    name = "songs_extrated"

    start_urls = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/"]

    npages = 2

    for i in range(2, npages + 2):
        start_urls.append("https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page="+str(i)+"")

    def parse(self, response):
        for href in response.xpath("//h4[contains(@class,'pt-cv-title')]/a[contains(@class,'_blank')]//@href"):
            url  = href.extract() 
            yield scrapy.Request(url, callback=self.parse_dir_contents)	
            
    def parse_dir_contents(self, response):
        item = SongItem()

        item['artist'] = response.xpath("//div[contains(@class,'su-column-inner su-u-clearfix su-u-trim')]/div/ul/li/span[contains(@class,'entry-categories')]/a[contains(@rel,'category tag')]/text()").extract()

        item['genre']= response.xpath("//span[contains(@class,'entry-tags')]/a[contains(@rel,'tag')]/descendant::text()").extract()

        item['lyricsBy'] = response.xpath("//span[contains(@class,'lyrics')]/a/descendant::text()").extract()

        item['musicBy'] = response.xpath("//span[contains(@class,'music')]/a/descendant::text()").extract()
        
        item['songTitle'] = response.xpath("//div[contains(@class,'entry-content')]/h2/descendant::text()").extract()

        item['key'] = response.xpath("//div[contains(@class,'entry-content')]/h3/descendant::text()").extract()

        item['artistName'] = response.xpath("//div[contains(@class,'entry-content')]/h6[contains(@class,'artist-name')]/descendant::text()").extract()

        item['movieName'] = response.xpath("//span[contains(@class,'movie')]/a/descendant::text()").extract()

        item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()

        songBody = (response.xpath('//div[@class="entry-content"]//pre/text()').extract())
        songBodySplit = []
        for parts in songBody:
            lines = parts.split('\n')
            for line in lines:
                songBodySplit.append(line)

        song = ""
        chords = ""

        for line in songBodySplit:
            if (re.search('[a-zA-Z]', line)):
                chords = chords + line + "\n"
            else:
                if (len(line) != 0):
                    line = line.replace('+', '')
                    line = line.replace('|', '')
                    line.strip()
                    song = song + line + os.linesep

        item['lyrics'] = song
     
        yield item

    def parse_item(self,response):
        with open('sinhala_songs-processed.json', 'w',encoding='utf-8') as f:
            f.write("".join(response.xpath('//body//*[not(self::script or self::style)]/text()').extract() ))
            item = SongItem()
            yield item
