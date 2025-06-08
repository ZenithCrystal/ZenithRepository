import requests
import json
import datetime
import os
import time
import random
from bs4 import BeautifulSoup

def get_google_news(query):
    """从Google搜索获取新闻"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws"
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for item in soup.select('div.SoaBEf'):
                title_element = item.select_one('div.mCBkyc')
                source_element = item.select_one('div.CEMjEf span')
                time_element = item.select_one('div.OSrXXb span')
                snippet_element = item.select_one('div.GI74Re')
                link_element = item.select_one('a')
                
                if title_element and link_element:
                    title = title_element.text
                    link = link_element.get('href')
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&')[0]
                    
                    source = source_element.text if source_element else "未知来源"
                    publish_time = time_element.text if time_element else "未知时间"
                    snippet = snippet_element.text if snippet_element else ""
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'source': source,
                        'publish_time': publish_time,
                        'snippet': snippet,
                        'origin': 'Google'
                    })
            
            return results
        else:
            print(f"Google搜索请求失败，状态码: {response.status_code}")
            return []
    except Exception as e:
        print(f"Google搜索过程中出错: {str(e)}")
        return []

def get_bing_news(query):
    """从Bing搜索获取新闻"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    search_url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for item in soup.select('.news-card'):
                title_element = item.select_one('.title')
                source_element = item.select_one('.source')
                time_element = item.select_one('.source span')
                snippet_element = item.select_one('.snippet')
                link_element = item.select_one('a.title')
                
                if title_element and link_element:
                    title = title_element.text
                    link = link_element.get('href')
                    
                    source = source_element.text.split('·')[0].strip() if source_element else "未知来源"
                    publish_time = time_element.text if time_element else "未知时间"
                    snippet = snippet_element.text if snippet_element else ""
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'source': source,
                        'publish_time': publish_time,
                        'snippet': snippet,
                        'origin': 'Bing'
                    })
            
            return results
        else:
            print(f"Bing搜索请求失败，状态码: {response.status_code}")
            return []
    except Exception as e:
        print(f"Bing搜索过程中出错: {str(e)}")
        return []

def collect_ai_news():
    """从多个来源收集AI新闻"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"正在收集{today}的AI新闻...")
    
    # 搜索查询关键词
    queries = [
        f"人工智能 新闻 {today}",
        f"AI news today {today}",
        "artificial intelligence latest developments",
        "机器学习 最新进展",
        "深度学习 突破",
        "GPT-4 news",
        "AI research breakthroughs"
    ]
    
    all_news = []
    
    # 从Google获取新闻
    for query in queries:
        print(f"正在从Google搜索: {query}")
        results = get_google_news(query)
        all_news.extend(results)
        # 添加随机延迟避免被封
        time.sleep(random.uniform(1.5, 3.5))
    
    # 从Bing获取新闻
    for query in queries:
        print(f"正在从Bing搜索: {query}")
        results = get_bing_news(query)
        all_news.extend(results)
        # 添加随机延迟避免被封
        time.sleep(random.uniform(1.5, 3.5))
    
    # 去重
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        if news['title'] not in seen_titles:
            seen_titles.add(news['title'])
            unique_news.append(news)
    
    # 按来源和时间排序
    sorted_news = sorted(unique_news, key=lambda x: (x['source'], x['publish_time']))
    
    print(f"成功收集到{len(sorted_news)}条独特的AI新闻")
    return sorted_news

def categorize_news(news_items):
    """对新闻进行简单分类"""
    categories = {
        "研究突破": [],
        "产品发布": [],
        "商业动态": [],
        "政策法规": [],
        "其他": []
    }
    
    # 简单的关键词分类
    keywords = {
        "研究突破": ["研究", "突破", "发现", "论文", "研发", "技术", "算法", "模型", "创新", "research", "breakthrough", "paper", "discovery", "algorithm", "model", "innovation"],
        "产品发布": ["发布", "推出", "产品", "版本", "更新", "应用", "软件", "工具", "release", "launch", "product", "version", "update", "application", "software", "tool"],
        "商业动态": ["公司", "企业", "投资", "融资", "市场", "收购", "合作", "伙伴", "company", "business", "investment", "funding", "market", "acquisition", "partnership"],
        "政策法规": ["政策", "法规", "监管", "合规", "法律", "规定", "标准", "政府", "policy", "regulation", "compliance", "legal", "standard", "government"]
    }
    
    for item in news_items:
        title_lower = item['title'].lower()
        snippet_lower = item['snippet'].lower() if item['snippet'] else ""
        
        categorized = False
        for category, words in keywords.items():
            for word in words:
                if word.lower() in title_lower or word.lower() in snippet_lower:
                    categories[category].append(item)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            categories["其他"].append(item)
    
    return categories

def generate_advanced_html(news_items):
    """生成更高级的HTML页面展示新闻"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # 对新闻进行分类
    categorized_news = categorize_news(news_items)
    
    # 读取HTML模板
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 生成分类新闻HTML
    news_html = ""
    
    for category, items in categorized_news.items():
        if items:  # 只显示有内容的分类
            news_html += f'<div class="category"><h2 class="category-title">{category}</h2>'
            
            for item in items:
                news_html += f"""
                <div class="news-item">
                    <h3><a href="{item['link']}" target="_blank">{item['title']}</a></h3>
                    <div class="news-meta">
                        <span class="source">{item['source']}</span>
                        <span class="time">{item['publish_time']}</span>
                        <span class="origin">{item['origin']}</span>
                    </div>
                    <p>{item['snippet']}</p>
                </div>
                """
            
            news_html += '</div>'
    
    # 替换模板中的占位符
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    today_with_time = f"{today} {current_time}"
    html_content = template.replace('{{DATE}}', today_with_time).replace('{{NEWS_ITEMS}}', news_html)
    
    # 写入HTML文件
    with open('ai_news.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成AI新闻页面: ai_news.html")
    return os.path.abspath('ai_news.html')

def main():
    """主函数"""
    print("高级AI新闻聚合器启动...")
    
    # 收集新闻
    news_items = collect_ai_news()
    
    if news_items:
        print(f"成功获取 {len(news_items)} 条AI新闻")
        # 生成HTML页面
        html_path = generate_advanced_html(news_items)
        print(f"新闻页面已生成: {html_path}")
        print("请在浏览器中打开此文件查看今日AI新闻")
    else:
        print("未能获取任何AI新闻，请检查网络连接或稍后再试")

if __name__ == "__main__":
    main()