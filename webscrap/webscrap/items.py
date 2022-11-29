# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time_stamp= scrapy.Field()
    site_details= scrapy.Field()
    name_of_site= scrapy.Field()
    food_groups_avilable= scrapy.Field()
    food_groups_details= scrapy.Field()
    
    food_group_navn= scrapy.Field()
    food_categories_avilable= scrapy.Field()

    food_categories_details= scrapy.Field()
    food_categories_navn= scrapy.Field()
    food_categories_images_url= scrapy.Field()
    food_categories_images_file= scrapy.Field()
    food_categories_images_download= scrapy.Field()

    food_sub_categories_avilable= scrapy.Field()
    
    food_sub_categories_details= scrapy.Field()
    food_sub_categorie_navn= scrapy.Field()
    product_details_avilable= scrapy.Field()
    product_details= scrapy.Field()

    product_name= scrapy.Field()
    #product_amount= scrapy.Field()
    product_short_description= scrapy.Field()
    product_description= scrapy.Field()
    product_aboutproduct= scrapy.Field()
    product_price= scrapy.Field()
    product_image_url= scrapy.Field()
    product_image_file= scrapy.Field()
       
    Astdns_anbefalers_avilable= scrapy.Field()
    Astdns_anbefalers_details= scrapy.Field()
    
    anbefalers_navn= scrapy.Field()
    anbefalers_promoimage= scrapy.Field()
    anbefalers_description=scrapy.Field()
    anbefalers_opskriftens_url= scrapy.Field()
    anbefalers_opskriftens_file= scrapy.Field()
    anbefalers_opskriftens_ingredients= scrapy.Field()
    ingredients_name= scrapy.Field()
    ingredients_detail= scrapy.Field()
    
    Astdns_kundeløfters= scrapy.Field()
    Astdns_fødevarestrategier_list= scrapy.Field()

    Astdns_fødevarestrategier= scrapy.Field()
    fødevarestrategi_navn1= scrapy.Field()
    fødevarestrategi_navn2= scrapy.Field()
    innovation_ogproduktudvikling_actions= scrapy.Field()
    innovation_ogproduktudvikling_details= scrapy.Field()

    bæredygtighed_ogmiljø_actions = scrapy.Field()
    bæredygtighed_ogmiljø_details= scrapy.Field()



    image_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
