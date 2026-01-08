import requests
from config import HEADERS,COOKIES,CATEGORY_ID,START_OFFSET,LIST_API_URL,DETAIL_URL_TEMPLATE,STOP_AFTER_ATTEMPT
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

class Crawler:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)
        self.session.verify = False

    def __del__(self):
        self.session.close()

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

    @retry(
        stop=stop_after_attempt(STOP_AFTER_ATTEMPT),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError
        )),
        reraise=True
    )
    def fetch_detail_page(self,post_id):
        """获取详情页原始HTML"""
        url = DETAIL_URL_TEMPLATE.format(post_id=post_id)
        resp = self.session.get(url,timeout=(5,10))

        if resp.status_code >= 500:
            resp.raise_for_status() # 触发重试
        elif resp.status_code>=400:
            return ""

        return resp.text