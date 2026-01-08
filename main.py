from crawler import Crawler
from storage import CSVStorage
from config import OUTPUT_FILE,START_OFFSET,END_OFFSET,BATCH_STEP,MAX_WORKERS,DETAIL_URL_TEMPLATE
from parser import parse_list_page,parse_publish_time,parse_detail_page
from utils import extract_post_id_from_url,random_delay
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def fetch_single_detail(task_data):
    """使用多线程并行解析多个讣告页面"""
    crawler = Crawler()
    post_id, title, raw_time = task_data

    try:
        detail_html = crawler.fetch_detail_page(post_id)
        content = parse_detail_page(detail_html) if detail_html else ""
    except Exception as e:
        print(f"❌ Detail failed for post={post_id} ({type(e).__name__}): {e}")
        content = ""
    finally:
        crawler.__del__()


    URL = DETAIL_URL_TEMPLATE.format(post_id=post_id)
    pub_time = parse_publish_time(raw_time)

    random_delay(0.3, 0.8)

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
        print(f"Fetching list page at offset {offset}...")

        try:
            list_html = crawler.fetch_list_page(offset)
            urls, titles, raw_times = parse_list_page(list_html)
        except Exception as e:
            print(f"⚠️ Skip offset {offset}: {e}")
            continue

        # 准备任务参数列表
        tasks_params = []
        for url,title,raw_time in zip(urls,titles,raw_times):
            post_id = extract_post_id_from_url(url)
            if post_id:
                tasks_params.append((post_id,title,raw_time)) # 存完所有帖子需要的参数开启多线程
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(fetch_single_detail,task_params) for task_params in tasks_params]

            for future in as_completed(futures):
                result = future.result()
                batch_data.append(result)

            # 批量保存
            if len(batch_data) >= BATCH_SIZE:
                storage.save_batch(batch_data)
                print(f"✅ Saved {len(batch_data)} items")
                batch_data = []
    # 保存剩余
    if batch_data:
        storage.save_batch(batch_data)
        print(f"✅ Final batch saved")

    print(f"Total time taken: {time.time() - start_time} seconds")
    print("🎉 All done!")

if __name__ == "__main__":
    main()