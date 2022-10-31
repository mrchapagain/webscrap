# -*- coding: utf-8 -*-

from webscrap.items import WebscrapItem
#from ..items import WebscrapItem 
import requests

import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import json
import posixpath
from urllib.parse import urljoin


def save_to_log_file(file_name, lik_source, link_to_save):
    with open (file_name, "a") as flog:
        flog.writelines("\n" + f"start of log file save '{lik_source}'"+ "\n")
        flog.writelines(map(lambda x: 'https://www.aarstiderne.com' + x + "\n", link_to_save)) #[page_link + "\n" for page_link in next_page_links])
        flog.writelines("\n" + f"end of log file save '{lik_source}'" + "\n")
        flog.writelines("\n" + "------------------------------------------------------------" + "\n")
        print("log file saved")

class ExtractUrls(scrapy.Spider):
    # This name must be unique always
    name = "webscrapfetch"     
    custom_settings = {'FEED_URI' : 'tmp/data.json'}  #location of file          
  
    # Function which will be invoked
    def start_requests(self):
        # enter the URL here
        allowed_domains = ['www.aarstiderne.com']
        start_urls = ['https://www.aarstiderne.com'] #, 'http://159.65.89.151/'http://en.wikipedia.org/https://citybazaar.dk/'http://159.65.89.151/'
        for start_url in start_urls:
            #This will return the response object and pass on next function "parse"
            yield scrapy.Request(url = start_url, callback = self.parse_frontpage_to_tabnavigation_page)

    
    def parse_frontpage_to_tabnavigation_page(self, response):

        # link for going to next pages from top nav-link
        next_page_from_topnavs = response.css('nav.topnav > ul.topnav__list > li > a::attr(href)').getall()

        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Front page to top-navvigation tab links', next_page_from_topnavs)

        for next_page_from_topnav in next_page_from_topnavs:
            
            if next_page_from_topnav == '/dagligvarer':
                #Initiate item class to save data
                items= WebscrapItem()

                # start to save data in item-dictionary object
                items['food_groups']= list(map(lambda x: x.strip() , response.css('nav#topnav > ul > li > a::text').getall()))
                yield items
    
                request= response.follow( url=next_page_from_topnav, callback=self.parse_foodgroup_pages )
                request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
                yield request
        #yield items

    

    def parse_foodgroup_pages(self, response):

        # link for going to next pages
        nextpage_category_links = response.css('div.prd-cats-nav__lst a::attr(href)').getall()

        """html_file= 'data.html'# to yield the initial response as HTML file and save it in HTML file
        with open (html_file, "wb") as fout:
            print("*" * 100)
            fout.write(response.body)
            print("*" * 100)"""

        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Front group to category page links', nextpage_category_links)
        
        #if nextpage_category_links is not None:
        for nextpage_category_link in nextpage_category_links:

            #call back item-dict object for saving data
            items= response.meta['items'] 

            # save data to item objects
            items['food_categories']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst a > h3::text').getall()
            items['food_images']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst > a > img::attr(src)').getall()
            yield items
 
            request= response.follow( url=nextpage_category_link, callback=self.parse_product_category_pages )
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request 
        #yield items

    
    def parse_product_category_pages(self, response):
    
        # link for going to next pages
        nextpage_product_subcategory_links = response.css('div.products > div.category-slider > a::attr(href)').extract()

        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Foof category to subcategory page links', nextpage_product_subcategory_links)

        for nextpage_product_subcategory_link in nextpage_product_subcategory_links:

            items = response.meta['items'] #Get the item we passed from scrape()
            # save data to item objects
            items['food_sub_categories']= response.css('div.products > div.category-slider > a::text').getall()
            yield items

            request= response.follow( url=nextpage_product_subcategory_link, callback=self.parse_product_subcategory_pages )
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            
            yield request 

        #yield items


    def parse_product_subcategory_pages(self, response):

        # link for going to next pages
        nextpage_product_detail_links = response.css('div.products > div.category-sections > sections > a::attr(href)').extract()

        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Food subcategory to products details page links', nextpage_product_detail_links)

        for nextpage_product_detail_link in nextpage_product_detail_links:
            items = response.meta['items'] #Get the item we passed from scrape()
            
            items['product_names']= response.css('div.product-sections > section.product-list > a > div.product-list__layout > header > h2::text').getall()
            yield items
                 
            request= response.follow( url=nextpage_product_detail_link, callback=self.parse_product_details_pages )
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request

        #yield items


    def parse_product_details_pages(self, response):

        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = response.css('li#menu-item-bundles > a::attr(href)').get()

        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Food product detail to Aarstidernes_anbefalers page links', nextpage_Aarstidernes_anbefalers_links)#Food product detail to metadata page links

        items = response.meta['items'] #Get the item we passed from scrape()

        items['product_names_tocheck']= response.css('div.products > div > div.product-details__actions > div > header > h1::text').get()
        items['product_amounts']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(4)::text').get()
        items['product_short_descriptions']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(5) > p::text').get() 
        items['product_descriptions']= response.css('div#product-details-section-description > div > div:nth-child(3) > p:nth-child(2)::text').get()
        items['product_aboutproducts']= response.css('div#product-details-section-description > div > div:nth-child(3) > *::text').getall() 
        items['product_prices']= response.css('div.product-list__layout > div.product-list__numbers > span:nth-child(1) > span.price::text').extract()
        items['product_images']= response.css('div#product-details-section-description > div > div.product-details__image > img::attr(src)').get()

        request= response.follow( url=nextpage_Aarstidernes_anbefalers_links, callback=self.parse_aarstidernes_anbefalers_pages )
        request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
        yield request



    def parse_aarstidernes_anbefalers_pages(self, response):
        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = response.css('section.bundle-overview > ul> li > a::attr(href)').getall()
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'products and company meta data', nextpage_Aarstidernes_anbefalers_links) #/jordens-bedste-koebmand/anbefalinger

        for nextpage_Aarstidernes_anbefalers_link in nextpage_Aarstidernes_anbefalers_links:
            items = response.meta['items'] #Get the item we passed from scrape()

            items['Aarstidernes_anbefalers']= response.css('ul.bundle-overview__list li::attr(data-alias)').getall()
            items['Aarstidernes_anbefalers_links']= response.css('ul.bundle-overview__list li > a::attr(href)').get()
            yield items
            
            request= response.follow( url=nextpage_Aarstidernes_anbefalers_link, callback=self.parse_aarstidernes_anbefalers_detail_pages )
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request
            

    def parse_aarstidernes_anbefalers_detail_pages(self, response):
        # link for going to next pages
        nextpage_metadata_links = ['https://www.aarstiderne.com/']
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'aarstidernes_anbefalers_detail to metadata', nextpage_metadata_links) # 

        items = response.meta['items'] #Get the item we passed from scrape()
        
        items['Aarstidernes_anbefalers_descriptions']= response.css('div.bundle__header--left > div.bundle__description > div p::text').getall()
        items['Aarstidernes_anbefalers_opskriftens_link']= response.css('div.bundle > header.bundle__header > div.bundle__header--left > p a::attr(href)').get()
        items['Aarstidernes_anbefalers_opskriftens_image']= response.css('main#main > div > div.bundle > header > div.bundle__header--right > section > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img::attr(src)').get()
        yield items
            
        request= response.follow( url=nextpage_metadata_links, callback=self.parse_product_company_metadata_pages )
        request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
        yield request

    def parse_product_company_metadata_pages(self, response):
        # link for going to next pages
        nextpage_finalpage_links = []
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'final page with metadata saving', nextpage_finalpage_links) 

        items = response.meta['items'] #Get the item we passed from scrape()

        items['Aarstidernes_kundeløfters']= response.css('ol.footer-promises__list  li::text').getall()

        # finally save all data to the file
        save_to_log_file('data.json', 'final dataset', {itm for itm in items})
        print("-"*50)
        yield items
        print("-"*50) 

        #scrapy runspider webscrapfetch.py -o link.xml

#process = CrawlerProcess()
#process.crawl(ExtractUrls)
#process.start()
        
