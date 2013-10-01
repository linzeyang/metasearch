# Create your views here.
import requests

class Item(object):
    def __init__(self, item_dict):
        self.title = item_dict["title"]
        self.url = item_dict["url"]
        self.displayurl = item_dict["displayurl"]
        self.snippet = item_dict.get("snippet", "<i>No snippet available for this item.</i>")
        self.source = ['EntireWeb']
        self.base_score = [0, 0, 0]
        self.weighted_score = 0.0
        
def getJsonObj(query, page_num, result_per_page):
    base_url = 'http://www.entireweb.com/xmlquery?pz=%s&ip=%s&q=%s&format=json&n=%s&of=%s'
    key = 'b954e0fe45f0929596268357988539e4'
    ip = '46.7.1.76'
    n = result_per_page
    of = (page_num - 1) * n
    url = base_url % (key, ip, query, n, of)
    
    return requests.get(url).json()
    
def getItemList(query, page_num, result_per_page):
    itemList = []
    jsonObj = getJsonObj(query, page_num, result_per_page)
    
    if not jsonObj:
        return []
        
    for i in jsonObj['hits']:
        itemList.append(Item(i))
        
    return itemList
