# 1.====== 基础网站信息配置 ======
# 1.1基础 URL
BASE_URL = "http://www.unitednews.net.ph/"
LIST_API_URL = f"{BASE_URL}getnews.php"
DETAIL_URL = "http://www.unitednews.net.ph/article.php"
DETAIL_URL_TEMPLATE = DETAIL_URL + "?post={post_id}" #模板

# 1.2请求头 & Cookie
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
# 1.3 爬取参数
CATEGORY_ID = "6"
BATCH_STEP = 5
START_OFFSET = 5
END_OFFSET = 100

# 2.====== 多线程爬取配置 ======
# 2.1最大并发线程数
MAX_WORKERS = 10

# 3.# ====== 文件存储配置 ======
# 3.1输出路径配置
OUTPUT_FILE = "obituaries.csv"

# 4.====== 重试机制配置 ======
# 4.1最大重试次数配置
STOP_AFTER_ATTEMPT = 3

# 5.====== Loguru 日志配置 ======
import sys
import os
from datetime import datetime
LOG_FILE = f"logs/app_{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.log"

# 可选：从环境变量读取控制台级别
CONSOLE_LEVEL = os.getenv("LOG_CONSOLE_LEVEL", "INFO")

LOGGER_HANDLERS = [
    # 控制台：简洁、彩色、INFO+
    {
        "sink": sys.stderr,
        "format": "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level:7}</lvl> | <c>{name}:{function}:{line}</c> | {message}",
        "colorize": True,
        "level": CONSOLE_LEVEL,
        "enqueue": True,
    },
    # 文件：详细、结构化、DEBUG+
    {
        "sink": LOG_FILE,
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:8} | {name}:{function}:{line:4} | {message}",
        "level": "DEBUG",
        "colorize": False,
        "rotation": "50 MB",
        "retention": "7 days",
        "encoding": "utf-8",
        "enqueue": True,
    }
]