# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class WebscrapPipeline:
    def process_item(self, item, spider):       
       
        # calling dumps to create json data.
        line = json.dumps(dict(item)) + "\n"  
        self.file.writelines(line + "\n")               
        return item
 
    def open_spider(self, spider):
        self.file = open('data.json', 'w')
 
    def close_spider(self, spider):
        self.file.close()


"""class ImagesPipeline:
    def process_item(self, image, spider):       
       
        # calling dumps to create json data.
        line = json.dumps(dict(image)) + "\n"  
        self.file.write(line)               
        return image
 
    def open_spider(self, spider):
        self.file = open('tmp/images/', 'w')
 
    def close_spider(self, spider):
        self.file.close()"""