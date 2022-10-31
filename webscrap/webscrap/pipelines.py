# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd
from datetime import datetime

class WebscrapPipeline:
    def process_item(self, item, spider):       
       
        # calling dumps to create json data.
        line=json.dumps(dict(item), ensure_ascii=True,  indent= '\t') + "\n"  
        my_dict= self.file.writelines(line + "\n")
        return my_dict
 
    def open_spider(self, spider):
        self.file = open('data.json', 'w')
 
    def close_spider(self, spider):
        self.file.close()
