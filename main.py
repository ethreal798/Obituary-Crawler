from crawler import Crawler
from storage import CSVStorage
from config import OUTPUT_FILE,START_OFFSET,END_OFFSET,BATCH_STEP,MAX_WORKERS,DETAIL_URL_TEMPLATE
from parser import parse_list_page,parse_publish_time,parse_detail_page
from utils import extract_post_id_from_url,random_delay
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from logger import logger
from tqdm import tqdm

def fetch_single_detail(task_data):
    """使用多线程并行解析多个讣告页面"""
    crawler = Crawler()
    post_id, title, raw_time = task_data

    try:
        detail_html = crawler.fetch_detail_page(post_id)
        content = parse_detail_page(detail_html) if detail_html else ""
    except Exception as e:
        logger.error(f"❌ Detail failed for post={post_id} ({type(e).__name__}): {e}")
        content = ""
    finally:
        crawler.__del__()

    URL = DETAIL_URL_TEMPLATE.format(post_id=post_id)
    pub_time = parse_publish_time(raw_time)

    random_delay(1, 3)

    return {
        "URL": URL,
        "Title": title,
        "Publish_Time": pub_time,
        "Content": content
    }

def main():
    start_time = time.time()
    crawler = Crawler()
    storage = CSVStorage(OUTPUT_FILE)
    batch_data = []
    BATCH_SIZE = 100

    for offset in range(START_OFFSET,END_OFFSET+1,BATCH_STEP):
        get_offset_data_time = time.time()
        logger.info(f"Fetching list page at offset {offset}...")
        try:
            # TODO 添加重试机制
            list_html = crawler.fetch_list_page(offset)
            urls, titles, raw_times = parse_list_page(list_html)
        except Exception as e:
            logger.error(f"⚠️ Skip offset {offset}: {e}")
            continue

        # 准备任务参数列表
        tasks_params = []
        for url,title,raw_time in zip(urls,titles,raw_times):
            post_id = extract_post_id_from_url(url)
            if post_id:
                tasks_params.append((post_id,title,raw_time)) # 存完所有帖子需要的参数开启多线程
        
        with (ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor):
            futures = [executor.submit(fetch_single_detail,task_params) for task_params in tasks_params]

            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"Processing Offset {offset:04d}",   # 如 "Offset 0100"
                unit="detail",                  # 单位显示为 "detail"
                ncols=80,                       # 进度条宽度
                leave=True,                     # 完成后保留最后一行
                colour='Green'                  # 进度条颜色：绿色
            ):
                result = future.result()
                batch_data.append(result)

            # 批量保存
            if len(batch_data) >= BATCH_SIZE:
                storage.save_batch(batch_data)
                logger.info(f"✅ Saved {len(batch_data)} items")
                batch_data = []
        logger.info(f"Finish This Offset:{offset} time taken: {round(time.time() - get_offset_data_time,3)} seconds")

    # 保存剩余
    if batch_data:
        storage.save_batch(batch_data)
        logger.info(f"✅ Final batch saved")

    logger.info(f"Total time taken: {time.time() - start_time} seconds")
    logger.info("🎉 All done!")

if __name__ == "__main__":
    main()