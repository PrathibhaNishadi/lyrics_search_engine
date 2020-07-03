# lyrics_search_engine
## Introduction
This is a simple search engine for searching song lyrics created using Elasticsearch and Node js for sinhala songs  
Data scraping and encoding is done by Python 

## Getting Started with Elasticsearch
### Setting up Elasticsearch

1. Download [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) and run the batch file  
   ( You can check if the server is up by browsing http://localhost:9200 )   
2. Optionally, download and run [Kibana](https://www.elastic.co/downloads/kibana) for query operations  

#### Data

The song details are in processed_song_details.json file containing 1096 objects containing 12 metadata  

```title``` : Name of the song (string)  
```artist``` : Singer of the song (string)  
```genre``` : Category of the song (string)  
```writer``` : Lyricist of the song (string)  
```composer``` : Music composer of the song (string)  
```views``` : Number of views for the song in original site (number)  
```beat``` : Beat of the music (string)  
```movie``` : Movie the song is in (string)  
```shares``` : How many shares happened in original site(number)  
```url``` : URL for the song in original site (string)  
```lyrics``` : lyrics of the song (string)  
```key``` : Key of the song and music  (string)  



##### Scraping

Python Scrapy is used for data scraping  
Data is scraped from the site www.sinhalasongbook.com  

##### Cleaning and processing

The unnecessary characters in the scraped data were removed and translated into sinhala using the googletrans Python library

### Creating Index

Used Kibana to create the index and mapping and tokenizing was done 

1. Create an index 'songs_new' and  using Kibana, execute the following  

Tokenizers

```
PUT /songs_new
{
         "settings": {
           "analysis": {
             "analyzer": {
               "new_analyzer": {
                 "type": "custom",
                 "tokenizer": "icu_tokenizer",
                 "filter": ["customNgram"]
               }
             },
              "filter":{
                   "customNgram":{
                       "type": "edge_ngram",
                       "min_gram":"4",
                       "max_gram": "18",
                       "side": "front"
                   }
             }
           }
         }
 }
```
2. Mapping  

```
PUT siongs_new/_mappings/
{
     properties:{
                     "artist" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "beat" : {
                         "type" : "text"
                     },
                     "composer" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "genre" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "key" : {
                         "type" : "text"
                     },
                     "movie" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "shares" : {
                         "type" : "long"
                     },
                     "songLyrics" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "songLyricsSearchable" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "title" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     },
                     "url" : {
                         "type" : "text"
                     },
                     "views" : {
                         "type" : "long"
                     },
                     "writer" : {
                         "type" : "text",
                         "fields" : {
                         "keyword" : {
                             "type" : "keyword"
                         }
                         },
                         "analyzer": "new_analyzer"
                     }
          }
}

```
## Getting started with Node js

Get all the dependencies installed using ```npm install``` command  

### Adding Documents to index

Run the command ```node data.js``` in the terminal to run the data.js file and add the documents  

### Starting Node server

1. Run the command ```node index.js``` in the terminal 
2. Browse http://localhost:3001 in the browser

## Start searching

Enter the search query in the search bar in sinhala language  

The frontend is built using Vue, HTML and CSS   

#### Basic Search  

>  Search by a song title  
> - Eg:- කොළොම් තොට  

> Search by an artist name  
> - Eg:- එඩ්වඩ් ජයකොඩි, එඩ්වඩ් ජයකොඩි ගැයූ  

> Search by a song genre  
> - Eg:- පැරණි පොප්ස්  

> Search by the lyricist  
> - Eg:- අජන්තා රණසිංහ රචිත 

> Search by the composer
> - Eg:- ඩබ්ලිව්.ඩී අමරදේව සංගීතවත් කල  

> Search by a lyrics  
> - Eg:- කොළොම් තොට නැත මහලු වී අවන්හල නැත පැරණි වී  

#### Advanced Search  
> Complex queries
> - Eg:- එඩ්වඩ් ජයකොඩි ගැයූ  හොඳම 10  
         ඩබ්ලිව්.ඩී අමරදේව කොළොම් තොට නැත මහලු වී  

## Filtering and Advanced Queries ( Boosting )

##### Filters has been used for artist, composer, lyricist and genre 
> Eg: Search query  "සුනිල්"  
> Results
>  Song details which contain  
> - "සුනිල්" in the lyrics  
> - "සුනිල්" in the lyricist  
> - "සුනිල්" in the artist  
> - "සුනිල්" in the composer  

##### Boosting has been used.

> Eg: If the phrase contains the word "රචිත" boost the lyricist field

##### Fuzzy search  

Fuzzy queries give results that are likely to be relevant for a particular search query  
This gives correct results even when spelling is not exactly the same  
> Eg: If we search "ක්ලැර" instead of "ක්ලැරන්ස්" this gives results same as when "ක්ලැරන්ස්" is given
