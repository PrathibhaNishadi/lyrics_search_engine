# lyrics_search_engine
## Introduction
This is a simple search engine for searching song lyrics created using Elasticsearch and Node js for sinhala songs  
Data scraping and encoding is done by Python 

## Getting Started with Elasticsearch
### Setting up Elasticsearch

1. Download Elasticsearch and run the batch file  
   ( You can check if the server is up by browsing http://localhost:9200 )   
2. Optionally, download and run Kibana for query operations  

#### Data

The song details are in processed_song_details.json file containing 1096 objects containing 12 metadata  
(Title, artist, lyricist, composer, beat, genre, movie, lyrics, views, url, shares and key) 

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
> Eg: එඩ්වඩ් ජයකොඩි, ඩබ්ලිව්.ඩී අමරදේව කොළොම් තොට නැත, එඩ්වඩ් ජයකොඩි ගැයූ  

The frontend is built using Vue, HTML and CSS   

## Filtering and Advanced Queries ( Boosting )

Filters has been used for artist, composer, lyricist and genre 
> Eg: Search query  "සුනිල්"  
> Results
>  Song details which contain  
> - "සුනිල්" in the lyrics  
> - "සුනිල්" in the lyricist  
> - "සුනිල්" in the artist  
> - "සුනිල්" in the composer  

Boosting has been used.

> Eg: If the phrase contains the word "රචිත" boost the lyricist field
