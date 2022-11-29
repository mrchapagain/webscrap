# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from slugify import slugify
import scrapy
from scrapy.exceptions import DropItem

import json
import datetime
import requests

"""class WebscrapPipeline:
    def process_item(self, item, spider):       
        # calling dumps to create json data.
        lines=json.dumps(dict(item), ensure_ascii=True,  indent= '\t')

        time_stamp= datetime.datetime.now()
        self.file.writelines(f'START ************************* New data started to register at: {time_stamp} *************************') 
        self.file.write("\n" + lines + '\n')
        self.file.writelines(f'************************* Data finished to register at: {time_stamp} ************************* END')

    def open_spider(self, spider):
        self.file = open('data.json', 'a', encoding='utf-8')
 
    def close_spider(self, spider):
        self.file.close()
 """




class WebscrapPipeline:    
    def process_item(self, item, spider):
        dict={}
        
        for key, val in item.items():
            dict[key]=val
        return dict

            #self.file.write("\n" + key + '\n')

    def open_spider(self, spider):
        self.file = open('data.json', 'a', encoding='utf-8')
 
    def close_spider(self, spider):
        self.file.close()

    #Have a look and test this
    """person_dict = {"name": "Bob",
    "languages": ["English", "French"],
    "married": True,
    "age": 32
    }

    with open('person.txt', 'w') as json_file:
        json.dump(person_dict, json_file)"""
 


"""class CustomImagesPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None,*, item=None):
        file_name= slugify("string", max_length=200)
        return f'full/{file_name}.jpg'
        
    def get_media_requests(self, item, info):
            for file_url in item['image_urls']:
                req= requests.get(file_url)
                return req"""
  
"""class FilesPipeline:
    def process_item(self, item, spider):      
        for file_url in item['food_categories_images_url']:
            req= requests.get(file_url)
            self.file.write(req.content)
 
    def open_spider(self, spider):
        self.file = open('data.PDF', 'wb')
 
    def close_spider(self, spider):
        self.file.close()"""
