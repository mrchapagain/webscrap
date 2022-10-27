from webscrap.items import WebscrapItem
#from ..items import WebscrapItem 
import requests
import scrapy
from scrapy import Selector
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
  
class ExtractUrls(scrapy.Spider):
      
    # This name must be unique always
    name = "webscrapfetch"     
    
    #location of file
    custom_settings = {
        'FEED_URI' : 'tmp/data.json'
    }            
  
    # Function which will be invoked
    def start_requests(self):
        # enter the URL here
        urls = ['https://www.aarstiderne.com/dagligvarer/'] #, 'http://159.65.89.151/'http://en.wikipedia.org/https://citybazaar.dk/'http://159.65.89.151/'
        for url in urls:
            #This will return the response object and pass on next function "parse"
            yield scrapy.Request(url = url, callback = self.parse_front)

    
    def parse_front(self, response):
        #yield the initial response as HTML file and save it in HTML file
        html_file= 'data.html'
        with open (html_file, "wb") as fout:
            print("*" * 100)
            fout.write(response.body)
            print("*" * 100)
    
        # link for going to next pages
        next_page_links = response.css('div.prd-cats-nav__lst a::attr(href)').extract()
        if next_page_links is not None:
            for next_page_link in next_page_links:
                url= "https://www.aarstiderne.com"
                next_page = url + next_page_link #response.urljoin(next_page_link)
                yield scrapy.Request(url=next_page, callback=self.parse_pages)
    
    def parse_pages(self, response):
        #yield the initial response as HTML file and save it in HTML file
        #link_file= 'link.html'
        #with open (link_file, "w") as flink:
            #print("*" * 100)
            #flink.write([link for link in response.body])
            #print("*" * 100)


        #Extracting the content for each category
        food_categories= response.css('.prd-cats-nav__lst-item-hdr::text').getall()
        food_cat_links= response.css('div.prd-cats-nav__lst a::attr(href)').extract()
        food_images= response.css('.prd-cats-nav__lst > a > img::attr(src)').extract()
        
        #extracting the image for food items from each category
        product_images= response.css('div.product-list__image > img::attr(src)').extract() 
        product_names= response.css('div.product-list__layout > header > h2::text').extract()
        product_descriptions= response.css('div.product-list__layout > div.product-list__short-description > span:nth-child(2)::text').extract()
        product_prices= response.css('div.product-list__layout > div.product-list__numbers > span:nth-child(1) > span.price::text').extract()
        product_details= response.css('div#product-details-section-description > div.product-details__description > div[itemprop~="description"] > p:nth-child(2)').extract()
        #response.xpath('div[@class="product-details-section-description"]/div[@class="product-details__description"]/div[contains(@itemprop,"description")]/p[1]').extract()
        #response.css('div#product-details-section-description > div.product-details__description > div:nth-of-type(1) > p:nth-of-type(2)').extract()
        
        
        Aarstidernes_kundeløfters= response.css('ol.footer-promises__list  li::text').extract()
        Aarstidernes_anbefalers= response.css('ul.bundle-overview__list li::attr(data-alias)').extract_first()
        Aarstidernes_anbefalers_descriptions= response.css('div.bundle__header--left > div.bundle__description > div p').extract()
        Aarstidernes_anbefalers_opskriftens= response.css('div.bundle > header.bundle__header > div.bundle__header--left > p a::attr(href)').extract()
        #response.css(' header > div.bundle__header--left > div.bundle__description > div > p:nth-child(1)').extract()
        Aarstidernes_anbefalers_links=response.css('ul.bundle-overview__list li > a::attr(href)').extract_first()
        
        #Initiate item class to save data
        items= WebscrapItem()
        #make a dictionary of data
        items['food_categories']= food_categories
        items['food_cat_links']= food_cat_links
        items['food_images']= food_images

        items['product_images']= product_images
        items['product_names']= product_names
        items['product_descriptions']= product_descriptions
        items['product_prices']= product_prices
        items['product_details']= product_details

        items['Aarstidernes_kundeløfters']= Aarstidernes_kundeløfters
        items['Aarstidernes_anbefalers']= Aarstidernes_anbefalers
        items['Aarstidernes_anbefalers_descriptions']= Aarstidernes_anbefalers_descriptions
        items['Aarstidernes_anbefalers_opskriftens']=Aarstidernes_anbefalers_opskriftens
        items['Aarstidernes_anbefalers_links']= Aarstidernes_anbefalers_links

        yield items

        #scrapy runspider webscrapfetch.py -o link.xml






#process = CrawlerProcess()
#process.crawl(ExtractUrls)
#process.start()
        
