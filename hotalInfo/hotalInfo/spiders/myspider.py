import scrapy
import json
import re
import random
import os
from urllib.parse import urlparse
from ..items import HotelItem

class WebsiteSourceSpider(scrapy.Spider):
    name = "website_source"
    start_urls = [
        'https://uk.trip.com/hotels/?locale=en-GB&curr=GBP',
    ]

    def __init__(self, *args, **kwargs):
        super(WebsiteSourceSpider, self).__init__(*args, **kwargs)
        self.image_directory = 'hotel_images'
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)
        

    def parse(self, response):
        script_content = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        
        if script_content:
            pattern = r'window\.IBU_HOTEL\s*=\s*(\{.*?\});'
            match = re.search(pattern, script_content, re.DOTALL)
            
            if match:
                ibu_hotel_data = match.group(1)
                ibu_hotel_dict = json.loads(ibu_hotel_data)

                categories = random.sample(['inboundCities', 'outboundCities', 'fiveStarHotels', 'cheapHotels', 'hostelHotels'], 3)

                for category in categories:
                    inList = ibu_hotel_dict['initData']['htlsData'][category]
                    
                    if category in ['inboundCities', 'outboundCities']:
                        yield from self.extract_data(inList[0]['recommendHotels'])
                    else:
                        yield from self.extract_data(inList)
                        
    def extract_data(self, hotels):
        for hotel in hotels:
            item = HotelItem()
            for k, v in hotel.items():
                if k in ['hotelId', 'hotelName', 'lat', 'lon', 'brief', 'imgUrl', 'cityName', 'fullAddress', 'hotelFacilityList']:
                    if k == 'imgUrl':
                        v = "https://ak-d.tripcdn.com/images/" + v
                        # Generate a unique filename for the image
                        filename = self.get_unique_filename(v)
                        filepath = os.path.join(self.image_directory, filename)
                        # Store the filepath instead of the URL
                        item[k] = filepath
                        # Download the image
                        yield scrapy.Request(v, callback=self.save_image, meta={'filepath': filepath, 'item': item})
                    elif k == 'hotelFacilityList':
                        v = [item['name'] for item in v]
                        item[k] = v
                    else:
                        item[k] = v
            
    def get_unique_filename(self, url):
        # Extract the filename from the URL and make it unique
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        name, ext = os.path.splitext(filename)
        return f"{name}_{random.randint(1000, 9999)}{ext}"

    def save_image(self, response):
        filepath = response.meta['filepath']
        with open(filepath, 'wb') as f:
            f.write(response.body)
        
        # Yield the item after the image has been saved
        yield response.meta['item']