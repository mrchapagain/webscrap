# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    food_categories= scrapy.Field()
    food_cat_links= scrapy.Field()
    food_images= scrapy.Field()
    product_images= scrapy.Field()
    product_names= scrapy.Field()
    product_descriptions= scrapy.Field()
    product_prices= scrapy.Field()
    product_details= scrapy.Field()
    Aarstidernes_kundeløfters= scrapy.Field()
    Aarstidernes_anbefalers= scrapy.Field()
    Aarstidernes_anbefalers_descriptions=scrapy.Field()
    Aarstidernes_anbefalers_opskriftens= scrapy.Field()
    Aarstidernes_anbefalers_links= scrapy.Field()
    #Aarstidernes_anbefalers_opskriftens= scrapy.Field()
