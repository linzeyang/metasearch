# Create your views here.
import requests

class Item(object):
    def __init__(self, item_dict):
        self.title = item_dict["url_title"]
        self.url = item_dict["url"]
        self.displayurl = item_dict["display_url"]
        self.snippet = item_dict.get("snippet", "<i>No snippet available for this item.</i>")
        self.source = ['Blekko']
        self.base_score = [0, 0, 0]
        self.weighted_score = 0.0
        
def getJsonObj(query, page_num, result_per_page):
    base_url = 'http://blekko.com/ws/?auth=%s&q=%s+/json+/ps=%s&p=%s'
    key = 'f4c8acf3'
    ps = result_per_page
    p = page_num - 1
    url = base_url % (key, query, ps, p)
    
    return requests.get(url).json()
    
def getItemList(query, page_num, result_per_page):
    itemList = []
    jsonObj = getJsonObj(query, page_num, result_per_page)
    
    if not jsonObj:
        return []
    
    for i in jsonObj["RESULT"]:
        itemList.append(Item(i))
        
    return itemList
