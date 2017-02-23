# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#encoding: utf-8
import os
def ParseFilePath(url):
    # user should change this folder path
    outfolder = "e:\\data\\FinTech\\News"
    components = url.split("/")
    year = components[3]
    monthday=components[4]
    month = monthday[:2]
    day = monthday[2:]
    idx=components[5]
    page=idx+"_"+components[6]
    folder = outfolder + "\\%s\\%s\\%s\\" % (year, month, day)
    filepath = folder + "%s.txt" % (page) 
    filepath=filepath.replace('?', '_')
    return(folder, filepath)

class Money163Pipeline(object):   
    def process_item(self, item, spider):
        if spider.name != "moneynews":  return item
        if item.get("news_thread", None) is None: return item
                
        url = item['news_url']
        folder, filepath = ParseFilePath(url)
        
        #one a single machine will is virtually no risk of race-condition
        if not os.path.exists(folder):
           os.makedirs(folder)        
        print(filepath)
        fo = open(filepath, 'w', encoding='utf')
        fo.write(str(dict(item)))
        fo.close()
        return None
        

