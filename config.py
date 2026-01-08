# 基础 URL
BASE_URL = "http://www.unitednews.net.ph/"
LIST_API_URL = f"{BASE_URL}getnews.php"
DETAIL_URL = "http://www.unitednews.net.ph/article.php"
DETAIL_URL_TEMPLATE = DETAIL_URL + "?post={post_id}" #模板

# 请求头 & Cookie
HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.unitednews.net.ph',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.unitednews.net.ph/category_page.php?category=6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

COOKIES = {
    '_ga': 'GA1.1.17021160.1766027272',
    '_ga_R6Q15675G4': 'GS2.1.s1766060425$o3$g1$t1766060628$j60$l0$h0',
}

# 爬取参数
CATEGORY_ID = "6"
BATCH_STEP = 5
START_OFFSET = 5
END_OFFSET = 100

# 最大并发线程数
MAX_WORKERS = 10

# 存储
OUTPUT_FILE = "obituaries.csv"

#最大重试次数
STOP_AFTER_ATTEMPT = 3