import requests
from config import HEADERS,COOKIES,CATEGORY_ID,START_OFFSET,LIST_API_URL,DETAIL_URL_TEMPLATE


class Crawler:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)
        self.session.verify = False

    def fetch_list_page(self,start_offset):
        """获取列表页原始HTML"""
        data = {
            'limit':20,
            'category':CATEGORY_ID,
            'start':START_OFFSET
        }

        resp = self.session.post(LIST_API_URL,data=data,timeout=10)
        resp.raise_for_status()
        return resp.text

    def fetch_detail_page(self,post_id):
        """获取详情页原始HTML"""
        url = DETAIL_URL_TEMPLATE.format(post_id=post_id)
        resp = self.session.get(url,params={"post":post_id},timeout=10)
        resp.raise_for_status()
        return resp.text