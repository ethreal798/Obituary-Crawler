# 讣告帖子爬取 - 菲律宾

一个结构清晰的 Python 爬虫，用于抓取菲律宾某网站上的讣告信息。

## 🌟 功能
- 抓取讣告标题、发布时间、正文内容等字段
- 支持保存为 CSV 文件（默认输出：`obituaries.csv`）
- **多线程解析页面，大幅提升抓取速度**
  - 可通过 `config.py` 调整并发线程数量
- **自动重试机制**：网络失败或服务器错误时自动重试，提升稳定性
  - 可通过 `config.py` 配置最大重试次数
- **实时进度条**：使用 `tqdm` 显示每批数据的抓取进度
- **结构化日志**：使用`loguru`记录关键运行信息，便于排查失败任务  
  - 日志级别和输出方式可通过 `config.py` 配置

## 🗂️ 项目架构
- `main.py`        — 程序入口
- `config.py`      — 配置管理（请求头、Cookie、目标 URL 等）
- `crawler.py`     — 网络请求模块（发送 HTTP 请求）
- `parser.py`      — 数据解析模块（从 HTML 提取结构化数据）
- `storage.py`     — 数据存储模块（写入 CSV 文件）
- `utils.py`       — 工具函数（如日期处理、文本清洗等）
- `logger.py`      — 日志初始化模块 (添加日志配置)

## ▶️ 使用方法

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行爬虫
python main.py