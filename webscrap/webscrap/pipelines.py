# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd
import datetime

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
