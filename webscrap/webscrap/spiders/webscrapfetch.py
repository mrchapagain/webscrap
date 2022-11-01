# -*- coding: utf-8 -*-

from webscrap.items import WebscrapItem
#from ..items import WebscrapItem 
import requests
import re

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
        flog.writelines("------------------------------------------------------------")
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
            yield scrapy.Request(url = start_url, callback = self.parse_frontpage_to_tabnavigation_page) # Output will be: <GET https://www.aarstiderne.com> (referer: None)

            # print to track what has been send to next page to scrap
            print("-"*50)
            print("Start URL at -start_requests function-: {} and request sent to next function -parse_frontpage_to_tabnavigation_page-: {}".format(start_url, start_urls))
            print("-"*50)

    
    def parse_frontpage_to_tabnavigation_page(self, response):
        # link for going to next pages from top nav-link
        next_page_from_topnavs = response.css('nav.topnav > ul.topnav__list > li > a::attr(href)').getall() # output will be: ['/find-din-maaltidskasse', '/vaelg-selv-retter', '/dagligvarer', '/jul-1', '/mortensaften']

        #Start to save links in the file by appending links
        save_to_log_file('log.jsonlines', 'Front page to top-navvigation tab links', next_page_from_topnavs)

        for next_page_from_topnav in next_page_from_topnavs:
            if next_page_from_topnav == "/dagligvarer":
                #Initiate item class (defined in items.py) to save data as dictionary format
                items= WebscrapItem()
                # start to save data in item-dictionary object
                items['food_groups']= list(map(lambda x: x.strip() , response.css('nav#topnav > ul > li > a::text').getall()))
                #yield items
    
                request= response.follow( url=next_page_from_topnav, callback=self.parse_foodgroup_pages ) # output will be: <GET https://www.aarstiderne.com/dagligvarer> (referer: None)
                request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
                
                # print to track what has been send to next page to scrap
                print("-"*50)
                print("Start URL at -parse_frontpage_to_tabnavigation_page- function: {} and request sent to next function -parse_foodgroup_pages-: {}".format(next_page_from_topnav, request))
                print("-"*50)
                
                yield request
    

    def parse_foodgroup_pages(self, response):
        # link for going to next pages
        nextpage_category_links = response.css('div.prd-cats-nav__lst a::attr(href)').getall() # output will be: ['/dagligvarer/frugt', '/dagligvarer/groent', '/dagligvarer/plantebaseret', '/dagligvarer/koed-fisk', '/dagligvarer/mejeri', '/dagligvarer/broed', '/dagligvarer/kolonial', '/dagligvarer/snacks-soede-sager', '/dagligvarer/juice-saft', '/dagligvarer/oel-vin', '/dagligvarer/husholdning-grej', '/dagligvarer/boger', '/jordens-bedste-koebmand/anbefalinger', '/dagligvarer/anbefalinger/hokkaidosuppe', '/dagligvarer/anbefalinger/pizza-bla-congo']
        save_to_log_file('log.jsonlines', 'Front group to category page links', nextpage_category_links) #save_to_log_file

        """html_file= 'data.html'# to yield the initial response as HTML file and save it in HTML file
        with open (html_file, "wb") as fout:
            print("*" * 100)
            fout.write(response.body)
            print("*" * 100)"""

        #if nextpage_category_links is not None:
        for nextpage_category_link in nextpage_category_links:
            #call back item-dict object for saving data
            items= response.meta['items'] 

            # save data to item objects
            items['food_categories']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst a > h3::text').getall()
            items['food_images']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst > a > img::attr(src)').getall()
            #yield items
 
            request= response.follow( url=nextpage_category_link, callback=self.parse_product_category_pages ) # output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            # print to track what has been send to next page to scrap
            print("-"*50)
            print("Start URL at -parse_foodgroup_pages- function: {} and request sent to next function -parse_product_category_pages-: {}".format(nextpage_category_link, request))
            print("-"*50)
            
            yield request 

    
    def parse_product_category_pages(self, response):
        # link for going to next pages
        nextpage_product_subcategory_links = response.css('div.products > div.category-slider > a::attr(href)').extract() # Output will be: ['/dagligvarer/frugt','/dagligvarer/frugt/frugtkasser','/dagligvarer/frugt/aebler-paerer','/dagligvarer/frugt/baer-druer','/dagligvarer/frugt/citrusfrugter','/dagligvarer/frugt/eksotiske-frugter', '/dagligvarer/frugt/blandede-frugtkasser']
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Foof category to subcategory page links', nextpage_product_subcategory_links)

        for nextpage_product_subcategory_link in nextpage_product_subcategory_links[1:]:
            items = response.meta['items'] #Get the item we passed from scrape()
            # save data to item objects
            items['food_sub_categories']= response.css('div.products > div.category-slider > a::text').getall()
            #yield items

            request= response.follow( url=nextpage_product_subcategory_link, callback=self.parse_product_subcategory_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt/frugtkasser> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            # print to track what has been send to next page to scrap
            print("-"*50)
            print("Start URL at -parse_product_category_pages- function: {} and request sent to next function -parse_product_subcategory_pages-: {}".format(nextpage_product_subcategory_link, request))
            print("-"*50)
            
            yield request 


    def parse_product_subcategory_pages(self, response):
        # link for going to next pages
        nextpage_product_detail_links = response.css('main#main > div > div.products > div.product-sections > section > a::attr(href)').getall() # Output will be: ['/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse','/dagligvarer/frugt/frugtkasser/friske-figner-2-kg','/dagligvarer/frugt/frugtkasser/avlernes-frugtkasse', '/dagligvarer/frugt/frugtkasser/aebler', '/dagligvarer/frugt/frugtkasser/fejokassen-4-kg', '/dagligvarer/frugt/frugtkasser/clementinkassen', '/dagligvarer/frugt/frugtkasser/eksotisk-frugtkasse', '/dagligvarer/frugt/frugtkasser/mangoposen', '/dagligvarer/frugt/frugtkasser/appelsinposen', '/dagligvarer/frugt/frugtkasser/citronposen']
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Food subcategory to products details page links', nextpage_product_detail_links)

        for nextpage_product_detail_link in nextpage_product_detail_links:
            items = response.meta['items'] #Get the item we passed from scrape()
            items['product_names']= response.css('div.product-sections > section.product-list > a > div.product-list__layout > header > h2::text').getall()
            #yield items
                 
            request= response.follow( url=nextpage_product_detail_link, callback=self.parse_product_details_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            # print to track what has been send to next page to scrap
            print("-"*50)
            print("Start URL at -parse_product_subcategory_pages- function: {} and request sent to next function -parse_product_details_pages-: {}".format(nextpage_product_detail_link, request))
            print("-"*50)

            yield request


    def parse_product_details_pages(self, response):
        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = response.css('li#menu-item-bundles > a::attr(href)').get() # Output will be: '/jordens-bedste-koebmand/anbefalinger'
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'Food product detail to Aarstidernes_anbefalers page links', nextpage_Aarstidernes_anbefalers_links)

        items = response.meta['items'] #Get the item we passed from scrape()

        items['product_names_tocheck']= response.css('div.products > div > div.product-details__actions > div > header > h1::text').get()
        items['product_amounts']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(4) >p::text').get()
        items['product_short_descriptions']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(5) > p > span::text').get()
        items['product_descriptions']= response.css('div#product-details-section-description > div > div:nth-child(3) > p:nth-child(2)::text').get()
        items['product_aboutproducts']= response.css('div#product-details-section-description > div > div:nth-child(3) > *::text').getall() 
        items['product_prices']= response.css('div.product-list__layout > div.product-list__numbers > span:nth-child(1) > span.price::text').extract()
        items['product_images']= response.css('div#product-details-section-description > div > div.product-details__image > img::attr(src)').get()

        request= response.follow( url=nextpage_Aarstidernes_anbefalers_links, callback=self.parse_aarstidernes_anbefalers_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/anbefalinger?redirect=1> from <GET https://www.aarstiderne.com/jordens-bedste-koebmand/anbefalinger>
        request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

        # print to track what has been send to next page to scrap
        print("-"*50)
        print("Start URL at -parse_product_details_pages- function: {} and request sent to next function -parse_aarstidernes_anbefalers_pages-: {}".format(nextpage_Aarstidernes_anbefalers_links, request))
        print("-"*50)

        yield request


    def parse_aarstidernes_anbefalers_pages(self, response):
        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = response.css('section.bundle-overview > ul> li > a::attr(href)').getall() # Output will be: ['/dagligvarer/anbefalinger/hokkaidosuppe', '/dagligvarer/anbefalinger/pizza-bla-congo', '/dagligvarer/anbefalinger/pizza-sod-kartoffel', '/dagligvarer/anbefalinger/hjemmelavet-frugtyoghurt', '/dagligvarer/anbefalinger/aarstidernes-lemonade', '/dagligvarer/anbefalinger/grillede-log', '/dagligvarer/anbefalinger/arroz-rejer-chorizo', '/dagligvarer/anbefalinger/fladbroed-med-hummus', '/dagligvarer/anbefalinger/svamperisotto', '/dagligvarer/anbefalinger/breakfast-sandwich', '/dagligvarer/anbefalinger/salade-nicoise', '/dagligvarer/anbefalinger/spaghetti-puttanesca', '/dagligvarer/anbefalinger/bibimbap-tempeh-kimchi', '/dagligvarer/anbefalinger/cocktails-gin', '/dagligvarer/anbefalinger/gron-juice', '/dagligvarer/anbefalinger/linsefars', '/dagligvarer/anbefalinger/pakoras', '/dagligvarer/anbefalinger/bag-selv-kit', '/dagligvarer/anbefalinger/bag-selv-rugbrod', '/dagligvarer/anbefalinger/tomatsalat-med-burrata', '/dagligvarer/anbefalinger/okonomiyaki', '/dagligvarer/anbefalinger/omelet-med-krautsalat', '/dagligvarer/anbefalinger/mexi-middag', '/dagligvarer/anbefalinger/sylt-selv-pickles']
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'products and company meta data', nextpage_Aarstidernes_anbefalers_links) #/jordens-bedste-koebmand/anbefalinger

        for nextpage_Aarstidernes_anbefalers_link in nextpage_Aarstidernes_anbefalers_links:
            items = response.meta['items'] #Get the item we passed from scrape()

            items['Aarstidernes_anbefalers']= response.css('ul.bundle-overview__list li::attr(data-alias)').getall()
            items['Aarstidernes_anbefalers_links']= response.css('ul.bundle-overview__list li > a::attr(href)').getall()
            items['Aarstidernes_anbefalers_opskriftens_promoimage']= response.css('ul.bundle-overview__list li::attr(style)').get() # Output should be like:
                    # now: 'background-image: url(/media/2095/jbk_anbefaling_hokkaidosuppe_primaert_2020_3053.jpg?crop=0,0,0,0&cropmode=percentage&width=900&height=675); background-color: #cf6227'
                    # shouls be like: https://www.aarstiderne.com/media/2095/jbk_anbefaling_hokkaidosuppe_primaert_2020_3053.jpg
            #yield items
            
            request= response.follow( url=nextpage_Aarstidernes_anbefalers_link, callback=self.parse_aarstidernes_anbefalers_detail_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/anbefalinger/hokkaidosuppe> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            # print to track what has been send to next page to scrap
            print("-"*50)
            print("Start URL at -parse_aarstidernes_anbefalers_pages- function: {} and request sent to next function -parse_aarstidernes_anbefalers_detail_pages-: {}".format(nextpage_Aarstidernes_anbefalers_link, request))
            print("-"*50)
            yield request
            

    def parse_aarstidernes_anbefalers_detail_pages(self, response):
        # link for going to next pages
        nextpage_metadata_links = ['https://www.aarstiderne.com/'] # Output will be:
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'aarstidernes_anbefalers_detail to metadata', nextpage_metadata_links) # 

        items = response.meta['items'] #Get the item we passed from scrape()
        
        items['Aarstidernes_anbefalers_descriptions']= response.css('div.bundle__header--left > div.bundle__description > div p::text').getall()
        items['Aarstidernes_anbefalers_opskriftens_link']= response.css('div.bundle > header.bundle__header > div.bundle__header--left > p a::attr(href)').get()
        #yield items
            
        request= response.follow( url=nextpage_metadata_links, callback=self.parse_product_company_metadata_pages ) # Output will be:
        request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

        # print to track what has been send to next page to scrap
        print("-"*50)
        print("Start URL at -parse_aarstidernes_anbefalers_detail_pages- function: {} and request sent to next function -parse_product_company_metadata_pages-: {}".format(nextpage_metadata_links, request))
        print("-"*50)

        yield request

    def parse_product_company_metadata_pages(self, response):
        # link for going to next pages
        nextpage_finalpage_links = [] # Output will be:
        #save_to_log_file
        save_to_log_file('log.jsonlines', 'final page with metadata saving', nextpage_finalpage_links) 

        items = response.meta['items'] #Get the item we passed from scrape()
        items['Aarstidernes_kundeløfters']= response.css('ol.footer-promises__list  li::text').getall()

        # print to track what has been send to next page to scrap
        print("-"*50)
        print("Start URL at -parse_product_company_metadata_pages- function: {} and request sent to next function -END HERE-: {}".format(response, items))
        print("-"*50)
        # finally save all data to the file
        save_to_log_file('data.json', 'final dataset', {itm for itm in items})

        yield items 
        

#scrapy runspider webscrapfetch.py -o link.xml

#process = CrawlerProcess()
#process.crawl(ExtractUrls)
#process.start()
        
