# 讣告帖子爬取 - 菲律宾

一个简单的 Python 爬虫，用于抓取菲律宾某网站上的讣告信息。

## 功能
- 抓取讣告标题、时间、内容等
- 支持保存为 CSV 文件

## 使用方法
```bash
# 创建虚拟环境并激活
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或者 .venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 运行爬虫
python main.py