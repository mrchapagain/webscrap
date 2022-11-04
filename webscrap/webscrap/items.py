# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    food_groups_avilable= scrapy.Field()
    
    food_group= scrapy.Field()
    food_categories_avilable= scrapy.Field()
    food_categories_images= scrapy.Field()

    food_categorie= scrapy.Field()
    food_sub_categories_avilable= scrapy.Field()
    
    food_sub_categorie= scrapy.Field()
    product_names_avilable= scrapy.Field()

    product_name= scrapy.Field()
    product_amount= scrapy.Field()
    product_short_description= scrapy.Field()
    product_description= scrapy.Field()
    product_aboutproduct= scrapy.Field()
    product_price= scrapy.Field()
    product_image= scrapy.Field()
       
    Aarstidernes_anbefalers_avilable= scrapy.Field()
    #####Aarstidernes_anbefalers_opskriftens_promoimage= scrapy.Field()

    Aarstidernes_anbefaler= scrapy.Field()
    Aarstidernes_anbefalers_description=scrapy.Field()
    Aarstidernes_anbefalers_opskriftens_link= scrapy.Field()
    Aarstidernes_anbefalers_opskriftens_ingredients_list= scrapy.Field()
    Aarstidernes_anbefalers_opskriftens_ingredient= scrapy.Field()
    
    Aarstidernes_kundeløfters= scrapy.Field()
    Aarstidernes_fødevarestrategier_list= scrapy.Field()

    Aarstidernes_fødevarestrategi= scrapy.Field()
    Aarstidernes_innovation_ogproduktudvikling= scrapy.Field()
    Aarstidernes_innovation_ogproduktudvikling_details= scrapy.Field()

    Aarstidernes_bæredygtighed_ogmiljø = scrapy.Field()
    Aarstidernes_ibæredygtighed_ogmiljø_details= scrapy.Field()
