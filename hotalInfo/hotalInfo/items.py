import scrapy

class HotelItem(scrapy.Item):
    hotelId = scrapy.Field()
    hotelName = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    brief = scrapy.Field()
    imgUrl = scrapy.Field()
    cityName = scrapy.Field()
    fullAddress = scrapy.Field()
    hotelFacilityList = scrapy.Field()