# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

import json
import pandas as pd
import datetime
import requests

class WebscrapPipeline:
    def process_item(self, item, spider):       
       
        # calling dumps to create json data.
        lines=json.dumps(dict(item), ensure_ascii=True,  indent= '\t')

        time_stamp= datetime.datetime.now()
        self.file.writelines(f'START ************************* New data started to register at: {time_stamp} *************************') 
        self.file.write("\n" + lines + "\n")
        self.file.writelines(f'************************* Data finished to register at: {time_stamp} ************************* END')
 
    def open_spider(self, spider):
        self.file = open('data.json', 'a')
 
    def close_spider(self, spider):
        self.file.close()

class MyImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item

"""def process_item(self, item, spider):   

        for file_url in item['food_categories_images_url']:
            req= requests.get(file_url)
            self.file.write(req.content)

 
    def open_spider(self, spider):
        self.file = open('data.PNG', 'wb')
 
    def close_spider(self, spider):
        self.file.close()"""




"""class FilesPipeline:
    def process_item(self, item, spider):      
        for file_url in item['food_categories_images_url']:
            req= requests.get(file_url)
            self.file.write(req.content)

 
    def open_spider(self, spider):
        self.file = open('data.PDF', 'wb')
 
    def close_spider(self, spider):
        self.file.close()"""


"""class DownfilesPipeline(FilesPipeline):
    def file_path(self, response, spider):
        file_url=response['food_categories_images_url']
        file_name= 'aarstiderne_hokkaidosuppe_v2_2020.pdf' #response['food_categories_images_file']
        req= 'https://www.aarstiderne.com/media/2100/aarstiderne_hokkaidosuppe_v2_2020.pdf'#requests.get(file_url)
        file_path= f'//WebScraping/webscrap/files/'
        with open(file_path, "wb") as f:
            f.write(req.content)
            f.write("check")

DownfilesPipeline()"""