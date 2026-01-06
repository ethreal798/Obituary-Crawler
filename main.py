from crawler import Crawler
from storage import CSVStorage
from config import OUTPUT_FILE,START_OFFSET,END_OFFSET,BATCH_STEP
from parser import parse_list_page,parse_publish_time,parse_detail_page
from utils import extract_post_id_from_url,random_delay

def main():
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

        for url, title, raw_time in zip(urls, titles, raw_times):
            post_id = extract_post_id_from_url(url)
            if not post_id:
                continue

            pub_time = parse_publish_time(raw_time)

            try:
                detail_html = crawler.fetch_detail_page(post_id)
                content = parse_detail_page(detail_html)
            except Exception as e:
                print(f"❌ Detail failed for post={post_id}: {e}")
                content = ""
            batch_data.append({
                "URL": f"http://www.unitednews.net.ph/?post={post_id}",
                "Title": title,
                "Publish_Time": pub_time,
                "Content": content
            })

            random_delay(0.3, 0.8)  # 可调小，因为已用 Session

            # 批量保存
            if len(batch_data) >= BATCH_SIZE:
                storage.save_batch(batch_data)
                print(f"✅ Saved {len(batch_data)} items")
                batch_data = []
    # 保存剩余
    if batch_data:
        storage.save_batch(batch_data)
        print(f"✅ Final batch saved")

    print("🎉 All done!")





if __name__ == "__main__":
    main()