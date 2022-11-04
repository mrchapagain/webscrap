# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    food_groups= scrapy.Field()

    food_categories= scrapy.Field()
    food_images= scrapy.Field()

    food_sub_categories= scrapy.Field()
    
    product_names= scrapy.Field()

    product_names_tocheck= scrapy.Field()
    product_amounts= scrapy.Field()
    product_short_descriptions= scrapy.Field()
    product_descriptions= scrapy.Field()
    product_aboutproducts= scrapy.Field()
    product_prices= scrapy.Field()
    product_images= scrapy.Field()
       
    Aarstidernes_anbefalers= scrapy.Field()
    Aarstidernes_anbefalers_links= scrapy.Field()
    #####Aarstidernes_anbefalers_opskriftens_promoimage= scrapy.Field()

    Aarstidernes_anbefalers_descriptions=scrapy.Field()
    Aarstidernes_anbefalers_opskriftens_link= scrapy.Field()
    
    Aarstidernes_kundeløfters= scrapy.Field()
    Aarstidernes_innovation_ogproduktudvikling= scrapy.Field()
    Aarstidernes_innovation_ogproduktudvikling_details= scrapy.Field()
    Aarstidernes_bæredygtighed_ogmiljø = scrapy.Field()
    Aarstidernes_ibæredygtighed_ogmiljø_details= scrapy.Field()
