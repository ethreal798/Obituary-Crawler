import random
import time

def extract_post_id_from_url(url):
    """从 '?post=123' 或 'page.php?post=123' 提取ID """
    if "post=" in url:
        return url.split("post=")[1].split("&")[0]
    return None

def random_delay(min_sec=0.5,max_sec=1.0):
    """模拟人类操作延迟"""
    time.sleep(random.uniform(min_sec,max_sec))