# -*- coding: utf-8 -*-

from webscrap.items import WebscrapItem
#from ..items import WebscrapItem 
import requests
import re
import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import json
from urllib.parse import urljoin
import datetime

def save_to_log_file(file_name, parce_func, start_urls, start_url, parce_urls, parce_to):
    with open(file_name, "a") as flog:
        flog.writelines("\n" + "START ------------------------------------------------------------" + "\n")
        flog.writelines(f"Function: {parce_func} with url: {start_url}" + "\n")
        flog.writelines("\t" + i for i in start_urls) #map(lambda x: 'https://www.aarstiderne.com' + x + "\n", start_url)
        flog.writelines("\n" + f"parce_urls: {parce_urls} to: {parce_to}"+ "\n")
        flog.writelines("------------------------------------------------------------ END" + "\n")
        
    # print to track what has been send to next page to scrap
    print("\n" + "START ------------------------------------------------------------")
    print(f"{file_name} saved at: {parce_func}")
    print(f"START url: {start_url} at: {parce_func}")
    print(f"parce_urls: {parce_urls} to: {parce_to}") 
    print("------------------------------------------------------------ END" + "\n")

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
            #Initiate item class (defined in items.py) to save data as dictionary format
            ##items= WebscrapItem()

            request= scrapy.Request(url = start_url, callback = self.parse_frontpage_to_tabnavigation_page) # Output will be: <GET https://www.aarstiderne.com> (referer: None)
            #This will return the response object and pass on next function "parse"
            yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "start_requests", start_urls, 'www.aarstiderne.com', request, "parse_frontpage_to_tabnavigation_page")
    
    def parse_frontpage_to_tabnavigation_page(self, response):
        # link for going to next pages from top nav-link
        next_page_from_topnavs = ['/dagligvarer'] 
        # response.css('nav.topnav > ul.topnav__list > li > a::attr(href)').getall() 
        # output will be: ['/find-din-maaltidskasse', '/vaelg-selv-retter', '/dagligvarer', '/jul-1', '/mortensaften']

        #Initiate item class (defined in items.py) to save data as dictionary format
        items= WebscrapItem()

        for next_page_from_topnav in next_page_from_topnavs:
            if next_page_from_topnav == "/dagligvarer":
                #call back item-dict object for saving data
                ##items= response.meta['items'] 

                # start to save data in item-dictionary object
                items['food_groups']= list(map(lambda x: x.strip() , response.css('nav#topnav > ul > li > a::text').getall()))
                #yield items
    
                request= response.follow( url=next_page_from_topnav, callback=self.parse_foodgroup_pages ) # output will be: <GET https://www.aarstiderne.com/dagligvarer> (referer: None)
                request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

                yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_frontpage_to_tabnavigation_page", next_page_from_topnavs, response, request, "parse_foodgroup_pages")
        
    
    def parse_foodgroup_pages(self, response):
        # link for going to next pages
        nextpage_category_links = ['/dagligvarer/frugt']
        # response.css('div.prd-cats-nav__lst a::attr(href)').getall() 
        # # output will be: ['/dagligvarer/frugt', '/dagligvarer/groent', '/dagligvarer/plantebaseret', '/dagligvarer/koed-fisk', '/dagligvarer/mejeri', '/dagligvarer/broed', '/dagligvarer/kolonial', '/dagligvarer/snacks-soede-sager', '/dagligvarer/juice-saft', '/dagligvarer/oel-vin', '/dagligvarer/husholdning-grej', '/dagligvarer/boger', '/jordens-bedste-koebmand/anbefalinger', '/dagligvarer/anbefalinger/hokkaidosuppe', '/dagligvarer/anbefalinger/pizza-bla-congo']

        #"""html_file= 'data.html'# to yield the initial response as HTML file and save it in HTML file
        #with open (html_file, "wb") as fout:
            #print("*" * 100)
            #fout.write(response.body)
            #print("*" * 100)"""

        #call back item-dict object for saving data
        items= response.meta['items'] 

        #if nextpage_category_links is not None:
        for nextpage_category_link in nextpage_category_links:
            #call back item-dict object for saving data
            ##items= response.meta['items'] 

            # save data to item objects
            items['food_categories']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst a > h3::text').getall()
            items['food_images']= response.css('section.prd-cats-nav > div.prd-cats-nav__lst > a > img::attr(src)').getall()
            #yield items
 
            request= response.follow( url=nextpage_category_link, callback=self.parse_product_category_pages ) # output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            
            yield request 

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_foodgroup_pages", nextpage_category_links, response, request, "parse_product_category_pages")

    
    def parse_product_category_pages(self, response):
        # link for going to next pages
        nextpage_product_subcategory_links = ['/dagligvarer/frugt/frugtkasser']
        #response.css('div.products > div.category-slider > a::attr(href)').getall() 
        # # Output will be: ['/dagligvarer/frugt','/dagligvarer/frugt/frugtkasser','/dagligvarer/frugt/aebler-paerer','/dagligvarer/frugt/baer-druer','/dagligvarer/frugt/citrusfrugter','/dagligvarer/frugt/eksotiske-frugter', '/dagligvarer/frugt/blandede-frugtkasser']

        items = response.meta['items'] #Get the item we passed from scrape()
        for nextpage_product_subcategory_link in nextpage_product_subcategory_links:#[1:]
            ##items = response.meta['items'] #Get the item we passed from scrape()
            # save data to item objects
            items['food_sub_categories']= response.css('div.products > div.category-slider > a::text').getall()
            #yield items

            request= response.follow( url=nextpage_product_subcategory_link, callback=self.parse_product_subcategory_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt/frugtkasser> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            
            yield request 

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_category_pages", nextpage_product_subcategory_links, response, request, "parse_product_subcategory_pages")


    def parse_product_subcategory_pages(self, response):
        # link for going to next pages
        nextpage_product_detail_links = ['/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse']
        #response.css('main#main > div > div.products > div.product-sections > section > a::attr(href)').getall() 
        # # Output will be: ['/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse','/dagligvarer/frugt/frugtkasser/friske-figner-2-kg','/dagligvarer/frugt/frugtkasser/avlernes-frugtkasse', '/dagligvarer/frugt/frugtkasser/aebler', '/dagligvarer/frugt/frugtkasser/fejokassen-4-kg', '/dagligvarer/frugt/frugtkasser/clementinkassen', '/dagligvarer/frugt/frugtkasser/eksotisk-frugtkasse', '/dagligvarer/frugt/frugtkasser/mangoposen', '/dagligvarer/frugt/frugtkasser/appelsinposen', '/dagligvarer/frugt/frugtkasser/citronposen']
        
        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_product_detail_link in nextpage_product_detail_links:
            ##items = response.meta['items'] #Get the item we passed from scrape()
            items['product_names']= response.css('div.product-sections > section.product-list > a > div.product-list__layout > header > h2::text').getall()
            #yield items
                 
            request= response.follow( url=nextpage_product_detail_link, callback=self.parse_product_details_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_subcategory_pages", nextpage_product_detail_links, response, request, "parse_product_details_pages")


    def parse_product_details_pages(self, response): # response from: <GET https://www.aarstiderne.com/dagligvarer/frugt/frugtkasser/dragefrugter-i-kasse>
        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = ['/dagligvarer/anbefalinger'] 
        #response.css('li#menu-item-bundles > a::attr(href)').getall()
        #Output will be: '/jordens-bedste-koebmand/anbefalinger'

        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_Aarstidernes_anbefalers_link in nextpage_Aarstidernes_anbefalers_links:
            ##items = response.meta['items'] #Get the item we passed from scrape()
            # start to saving dat in items object
            items['product_names_tocheck']= response.css('div.products > div > div.product-details__actions > div > header > h1::text').get()
            items['product_amounts']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(4) >p::text').get()
            items['product_short_descriptions']= response.css('div.products > div > div.product-details__actions > div > div:nth-child(5) > p > span::text').get()
            items['product_descriptions']= response.css('div#product-details-section-description > div > div:nth-child(3) > p:nth-child(2)::text').get()
            items['product_aboutproducts']= response.css('div#product-details-section-description > div > div:nth-child(3) > *::text').getall() 
            items['product_prices']= response.css('div.product-list__layout > div.product-list__numbers > span:nth-child(1) > span.price::text').extract()
            items['product_images']= response.css('div#product-details-section-description > div > div.product-details__image > img::attr(src)').get()
            #yield items
            
            
            request= response.follow( url=nextpage_Aarstidernes_anbefalers_link, callback=self.parse_aarstidernes_anbefalers_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/anbefalinger> (referer: None)
            #<GET https://www.aarstiderne.com/dagligvarer/anbefalinger?redirect=1> from <GET https://www.aarstiderne.com/jordens-bedste-koebmand/anbefalinger>
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            
            yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_details_pages", nextpage_Aarstidernes_anbefalers_links, response, request, "parse_aarstidernes_anbefalers_pages")


    def parse_aarstidernes_anbefalers_pages(self, response): # Response from: <GET https://www.aarstiderne.com/dagligvarer/anbefalinger> 
        # link for going to next pages
        nextpage_Aarstidernes_anbefalers_links = ['/dagligvarer/anbefalinger/hokkaidosuppe']
        #response.css('section.bundle-overview > ul> li > a::attr(href)').getall() 
        # # Output will be: ['/dagligvarer/anbefalinger/hokkaidosuppe', '/dagligvarer/anbefalinger/pizza-bla-congo', '/dagligvarer/anbefalinger/pizza-sod-kartoffel', '/dagligvarer/anbefalinger/hjemmelavet-frugtyoghurt', '/dagligvarer/anbefalinger/aarstidernes-lemonade', '/dagligvarer/anbefalinger/grillede-log', '/dagligvarer/anbefalinger/arroz-rejer-chorizo', '/dagligvarer/anbefalinger/fladbroed-med-hummus', '/dagligvarer/anbefalinger/svamperisotto', '/dagligvarer/anbefalinger/breakfast-sandwich', '/dagligvarer/anbefalinger/salade-nicoise', '/dagligvarer/anbefalinger/spaghetti-puttanesca', '/dagligvarer/anbefalinger/bibimbap-tempeh-kimchi', '/dagligvarer/anbefalinger/cocktails-gin', '/dagligvarer/anbefalinger/gron-juice', '/dagligvarer/anbefalinger/linsefars', '/dagligvarer/anbefalinger/pakoras', '/dagligvarer/anbefalinger/bag-selv-kit', '/dagligvarer/anbefalinger/bag-selv-rugbrod', '/dagligvarer/anbefalinger/tomatsalat-med-burrata', '/dagligvarer/anbefalinger/okonomiyaki', '/dagligvarer/anbefalinger/omelet-med-krautsalat', '/dagligvarer/anbefalinger/mexi-middag', '/dagligvarer/anbefalinger/sylt-selv-pickles']
        
        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_Aarstidernes_anbefalers_link in nextpage_Aarstidernes_anbefalers_links:
            ##items = response.meta['items'] #Get the item we passed from scrape()

            items['Aarstidernes_anbefalers']= response.css('ul.bundle-overview__list li::attr(data-alias)').getall()
            items['Aarstidernes_anbefalers_links']= response.css('ul.bundle-overview__list li > a::attr(href)').getall()
            #####items['Aarstidernes_anbefalers_opskriftens_promoimage']= response.css('ul.bundle-overview__list li::attr(style)').get() # Output should be like:
            # now: 'background-image: url(/media/2095/jbk_anbefaling_hokkaidosuppe_primaert_2020_3053.jpg?crop=0,0,0,0&cropmode=percentage&width=900&height=675); background-color: #cf6227'
            # shouls be like: https://www.aarstiderne.com/media/2095/jbk_anbefaling_hokkaidosuppe_primaert_2020_3053.jpg
            #yield items
            
            request= response.follow( url=nextpage_Aarstidernes_anbefalers_link, callback=self.parse_aarstidernes_anbefalers_detail_pages ) # Output will be: <GET https://www.aarstiderne.com/dagligvarer/anbefalinger/hokkaidosuppe> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_aarstidernes_anbefalers_pages", nextpage_Aarstidernes_anbefalers_links, response, request, "parse_aarstidernes_anbefalers_detail_pages")
            

    def parse_aarstidernes_anbefalers_detail_pages(self, response):   # response from <GET https://www.aarstiderne.com/dagligvarer/anbefalinger/hokkaidosuppe>
        # link for going to next pages
        nextpage_metadata_links = ['/om-aarstiderne']
        #response.css('div.header__top > nav > ul > li:nth-child(6) > a::attr(href)').getall() 
        # # Output will be: ['/om-aarstiderne']

        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_metadata_link in nextpage_metadata_links:
            ##items = response.meta['items'] #Get the item we passed from scrape()
            items['Aarstidernes_anbefalers_descriptions']= response.css('div.bundle__header--left > div.bundle__description > div p::text').getall()
            items['Aarstidernes_anbefalers_opskriftens_link']= response.css('div.bundle > header.bundle__header > div.bundle__header--left > p a::attr(href)').getall()
            #yield items
                
            request= response.follow( url=nextpage_metadata_link, callback=self.parse_product_company_metadata_pages_1 ) # Output will be: <GET https://www.aarstiderne.com/om-aarstiderne> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.

            yield request

        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_aarstidernes_anbefalers_detail_pages", nextpage_metadata_links, response, request, "parse_product_company_metadata_pages_1")

    
    
    def parse_product_company_metadata_pages_1(self, response): # response from <GET https://www.aarstiderne.com/om-aarstiderne> 
        # link for going to next pages
        nextpage_finalpage_links = ['/om-aarstiderne/baeredygtighed-og-miljoe']
        #['/om-aarstiderne/baeredygtighed-og-miljoe', '/om-aarstiderne/innovation-og-produktudvikling'] # use how to select multiple nth in css selector
        # response.css('div.products-bg > section > article > nav > div:nth-child(4-5) > a::attr(href)').getall() 
        # # Output will be: ['/om-aarstiderne/baeredygtighed-og-miljoe', '/om-aarstiderne/innovation-og-produktudvikling']

        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_finalpage_link in nextpage_finalpage_links:
            items['Aarstidernes_kundeløfters']= response.css('ol.footer-promises__list  li::text').getall()
                
            request= response.follow( url=nextpage_finalpage_link, callback=self.parse_product_company_metadata_pages_2 ) # Output will be: <GET https://www.aarstiderne.com/om-aarstiderne/baeredygtighed-og-miljoe> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request
        
        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_company_metadata_pages_1", nextpage_finalpage_links, response, request, "parse_product_company_metadata_pages_2")


    
    def parse_product_company_metadata_pages_2(self, response): # response from <GET https://www.aarstiderne.com/om-aarstiderne/baeredygtighed-og-miljoe>
        # link for going to next pages
        nextpage_finalpage_links = ['/om-aarstiderne/innovation-og-produktudvikling']
        
        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_finalpage_link in nextpage_finalpage_links:
            
            items['Aarstidernes_bæredygtighed_ogmiljø']= list(map(lambda x: x.strip() , response.css('div.products-bg > section > article > nav div > a > h2 *::text').getall()))
            items['Aarstidernes_ibæredygtighed_ogmiljø_details']= response.css('div.products-bg > section > article > nav div > a > div *::text').getall()

            #items['Aarstidernes_innovation_ogproduktudvikling']= response.css('section.article > article > ul  li >a > div > h2 *::text').getall()
            #items['Aarstidernes_innovation_ogproduktudvikling_details']= response.css('section.article > article > ul  li >a > div > div *::text').getall()
            
            #yield items
                
            request= response.follow( url=nextpage_finalpage_link, callback=self.parse_product_company_metadata_pages_3 ) # Output will be: <GET https://www.aarstiderne.com/om-aarstiderne/innovation-og-produktudvikling> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request
        
        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_company_metadata_pages_2", nextpage_finalpage_links, response, request, "parse_product_company_metadata_pages_3")
    
    
    def parse_product_company_metadata_pages_3(self, response): # response from <GET https://www.aarstiderne.com/om-aarstiderne/innovation-og-produktudvikling>
        # link for going to next pages
        nextpage_finalpage_links = ['/om-aarstiderne/baggrund-og-tal/aarstidernes-5-loefter']
        
        items = response.meta['items'] #Get the item we passed from scrape()

        for nextpage_finalpage_link in nextpage_finalpage_links:

            items['Aarstidernes_innovation_ogproduktudvikling']= response.css('section.article > article > ul  li >a > div > h2 *::text').getall()
            items['Aarstidernes_innovation_ogproduktudvikling_details']= response.css('section.article > article > ul  li >a > div > div *::text').getall()
            
            #yield items
                
            request= response.follow( url=nextpage_finalpage_link, callback=self.parse_data_save_pages ) # Output will be: <GET https://www.aarstiderne.com/om-aarstiderne/baggrund-og-tal/aarstidernes-5-loefter> (referer: None)
            request.meta['items'] = items #By calling .meta, we can pass our item object into the callback.
            yield request
        
        # Save information to log file and print print
        save_to_log_file('log.jsonlines', "parse_product_company_metadata_pages_3", nextpage_finalpage_links, response, request, "parse_data_save_pages")


    
    def parse_data_save_pages(self, response): # Response from: <GET https://www.aarstiderne.com/om-aarstiderne/baggrund-og-tal/aarstidernes-5-loefter>
        #Get the item we passed from scrape()
        items = response.meta['items'] 

        # Finally save all the yield items to the file
        json_file= 'backup.json'
        with open(json_file, "wb") as fout:
            print(items)
            print("*" * 50)
            print("It reaches to data saving function-before dump")
            #lines=json.dumps(dict(items), ensure_ascii=True,  indent= '\t') + "\n" 
            print("It reaches to data saving function-after dump")
            print("Type of items:", type(items))
            #print("Type of Lines:", type(lines)) 
            #fout.write("\n" + lines + "\n")
            print("Data has been saved to data.json file")
            print("*" * 50)


        yield items 
        

#scrapy runspider webscrapfetch.py -o link.xml

#process = CrawlerProcess()
#process.crawl(ExtractUrls)
#process.start()
        
