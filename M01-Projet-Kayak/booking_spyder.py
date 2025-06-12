#library
import os  #folder and path
import logging  #process
import scrapy   
from scrapy.crawler import CrawlerProcess   #follow urls
import pandas as pd


#create a dataframe with urls and city_id
df_cities = pd.read_csv('../data/Kayak/cities.csv')

class Booking_spyder(scrapy.Spider):
    name = 'booking'

    # for using url and city_id from dataframe
    def start_requests(self):
        for index, row in df_cities.iterrows():
            url = row['url']
            city_id = row['city_id']
            yield scrapy.Request(url=url, callback=self.parse, meta={'city_id': city_id})



    # crawling on the main page
    def parse(self, response):
        city_id = response.meta['city_id']    #for passing the city_id

        #the main layout in the result page with hostel data
        hostels = response.xpath('//div[contains(@data-testid, "property-card")]') 

        #crawling data in all hostels from the result page
        for hostel in hostels:
            #to be crawled
            name = hostel.xpath('.//div[@data-testid="title"]/text()').get().strip()
            rating = hostel.xpath('.//div[@data-testid="review-score"]/div/text()').get()
            url_to_follow = hostel.xpath('.//a[@data-testid="title-link"]/@href').get()   #url to follow for more data

            yield response.follow(url_to_follow, self.parse_hotel, meta={'name' : name, 'rating' : rating, 'url': url_to_follow, 'city_id' : city_id})

    # crawling on the hotel page
    def parse_hotel(self, response):
        
        # already crawled in result page
        name = response.meta['name']
        rating = response.meta['rating']
        url_to_follow = response.meta['url']
        city_id = response.meta['city_id']

        
        #to be crawled in hostel page
        gps = response.xpath('//a[@id="map_trigger_header"]/@data-atlas-latlng').get()
        lat, lon = gps.split(",", 1)
        desc = response.xpath('.//p[@data-testid="property-description"]/text()').get().strip()

        # 
        yield {
            'name' : name,
            'rating': rating,
            'lat': lat,
            'lon':lon, 
            'desc': desc,
            'url': url_to_follow,
            'city_id' : city_id
            }


# Path and filename
path = '../data/Kayak/'
filename = 'list_hostels.json'

#deleting old file if exist
if filename in os.listdir(path):
    os.remove(path + filename)


process = CrawlerProcess(settings = {
'USER_AGENT': 'Chrome/97.0',
'LOG_LEVEL': logging.INFO,
"FEEDS": {
path  + filename : {"format": "json"},
}
})

# Start the crawling using the spider you defined above
process.crawl(Booking_spyder)
process.start()