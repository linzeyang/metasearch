import requests


class Api(object):

    @classmethod
    def get_json_obj(cls, query, page_num, result_per_page):
        raise NotImplementedError

    @classmethod
    def get_item_list(cls, query, page_num, result_per_page):
        raise NotImplementedError


class BingApi(Api):

    def __init__(self, item_dict):
        self.title = item_dict["Title"]
        self.url = item_dict["Url"]
        self.displayurl = item_dict["DisplayUrl"]
        self.snippet = item_dict.get(
            "Description", "<i>No snippet available for this item.</i>")
        self.source = ['BING']
        self.base_score = [0, 0, 0]
        self.weighted_score = 0.0

    @classmethod
    def get_json_obj(cls, query, page_num, result_per_page):
        base_url = "https://api.datamarket.azure.com/Bing/SearchWeb/Web"
        base_url += "?Query=%27{}%27&$format=json&$top={}&$skip={}"
        key = 'tQbZUHxsuy+lQ+ud5WoXJMh4Ebl51WQx2wtbIkPKnBE='
        top = result_per_page
        skip = (page_num - 1) * top
        url = base_url.format(query, top, skip)

        return requests.get(url, auth=('', key)).json()

    @classmethod
    def get_item_list(cls, query, page_num, result_per_page):
        item_list = []
        json_obj = cls.get_json_obj(query, page_num, result_per_page)

        for i in json_obj["d"]["results"]:
            item_list.append(cls(i))

        return item_list


class BlekkoApi(Api):

    def __init__(self, item_dict):
        self.title = item_dict["url_title"]
        self.url = item_dict["url"]
        self.displayurl = item_dict["display_url"]
        self.snippet = item_dict.get(
            "snippet", "<i>No snippet available for this item.</i>")
        self.source = ['Blekko']
        self.base_score = [0, 0, 0]
        self.weighted_score = 0.0

    @classmethod
    def get_json_obj(cls, query, page_num, result_per_page):
        base_url = 'http://blekko.com/ws/?auth={}&q={}+/json+/ps={}&p={}'
        key = 'f4c8acf3'
        ps = result_per_page
        p = page_num - 1
        url = base_url.format(key, query, ps, p)

        return requests.get(url).json()

    @classmethod
    def get_item_list(cls, query, page_num, result_per_page):
        item_list = []
        json_obj = cls.get_json_obj(query, page_num, result_per_page)

        if not json_obj:
            return []

        for i in json_obj["RESULT"]:
            item_list.append(cls(i))

        return item_list


class EntwebApi(Api):

    def __init__(self, item_dict):
        self.title = item_dict["title"]
        self.url = item_dict["url"]
        self.displayurl = item_dict["displayurl"]
        self.snippet = item_dict.get(
            "snippet", "<i>No snippet available for this item.</i>")
        self.source = ['EntireWeb']
        self.base_score = [0, 0, 0]
        self.weighted_score = 0.0

    @classmethod
    def get_json_obj(cls, query, page_num, result_per_page):
        base_url = "http://www.entireweb.com/xmlquery"
        base_url += "?pz={}&ip={}&q={}&format=json&n={}&of={}"
        key = 'b954e0fe45f0929596268357988539e4'
        ip = '46.7.1.76'
        n = result_per_page
        of = (page_num - 1) * n
        url = base_url.format(key, ip, query, n, of)

        return requests.get(url).json()

    @classmethod
    def get_item_list(cls, query, page_num, result_per_page):
        item_list = []
        json_obj = cls.get_json_obj(query, page_num, result_per_page)

        if not json_obj:
            return []

        for i in json_obj['hits']:
            item_list.append(cls(i))

        return item_list
