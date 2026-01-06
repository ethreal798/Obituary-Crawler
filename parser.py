from datetime import datetime
from lxml import html

def parse_list_page(html_text):
    """解析列表页，返回（urls,titles,times）"""
    try:
        doc = html.fromstring(html_text)
    except Exception as e:
        raise ValueError(f"Failed to parse list page:{e}")

    urls = doc.xpath("//a/@href")
    titles = [t.strip() for t in doc.xpath("//div[@class='thumbs-title-container']/h5/text()")]
    raw_times = [t.strip() for t in doc.xpath("//small/text()")]

    # 对齐长度
    min_len = min(len(urls), len(titles), len(raw_times))
    return urls[:min_len], titles[:min_len], raw_times[:min_len]

def parse_detail_page(html_text):
    """解析详情页，返回纯文本内容"""
    try:
        doc = html.fromstring(html_text)
        content_nodes = doc.xpath(
            "//div[contains(@class, 'article-content')]//p//text() | "
            "/html/body/div[3]/div[2]/div[2]/div/div/div[2]/div/div[3]/p//text()"
        )
        return ''.join(content_nodes).strip()
    except Exception as e:
        raise ValueError(f"Failed to parse detail page:{e}")

def parse_publish_time(raw_time_str):
    """解析 'December 16, 2025' 格式日期"""
    try:
        return datetime.strptime(raw_time_str,"%B %d, %Y")
    except ValueError:
        return None