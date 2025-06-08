import requests
import json
import datetime
import os
import random
import time
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator # 导入翻译库
import re # 导入正则表达式模块

def contains_chinese(text):
    """检查字符串是否包含中文字符。"""
    if not text or not isinstance(text, str):
        return False
    # 中文字符的Unicode范围
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def translate_text_to_chinese(text, target_language='zh-CN'):
    """将文本翻译成中文，如果已经是中文或翻译失败，则返回原文。"""
    if not text or not isinstance(text, str):
        return text # 如果文本为空或不是字符串，直接返回
    
    # 如果文本已经包含中文，则直接返回
    if contains_chinese(text):
        # print(f"  - 文本已包含中文，无需翻译: '{text[:50]}...'") # 可以取消注释以进行调试
        return text
        
    try:
        # 尝试自动检测源语言并翻译到目标语言
        # GoogleTranslator 会自动检测源语言
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        if translated_text and translated_text.strip():
            return translated_text
        else:
            # 如果翻译结果为空，可能意味着已经是目标语言或无法翻译
            return text
    except Exception as e:
        print(f"  - 翻译文本时出错: '{text[:50]}...' - {str(e)}")
        # 确保即使翻译出错也返回原始文本，避免None或异常中断流程
        return text if text else "" # 如果text本身是None，返回空字符串

def search_ai_news():
    """使用网络搜索获取今日AI新闻"""
    print("正在搜集AI新闻...")
    
    # 获取今天的日期
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
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
    
    # 尝试多个新闻源
    news_sources = [
        {"function": search_google, "name": "Google搜索"},
        {"function": search_bing, "name": "Bing搜索"},
        {"function": get_ai_news_from_alternative, "name": "备用新闻源"}
    ]
    
    # 随机打乱顺序，避免总是使用同一个源
    random.shuffle(news_sources)
    
    all_news = []
    
    # 依次尝试不同的新闻源
    for source in news_sources:
        print(f"尝试从{source['name']}获取新闻...")
        
        # 对于搜索引擎，尝试多个查询关键词
        if source['name'] in ["Google搜索", "Bing搜索"]:
            for query in queries:
                try:
                    print(f"  - 搜索: {query}")
                    news_items = source['function'](query)
                    if news_items and len(news_items) > 0:
                        all_news.extend(news_items)
                        print(f"  - 获取到{len(news_items)}条新闻")
                    # 添加随机延迟避免被封
                    time.sleep(random.uniform(1.0, 2.5))
                except Exception as e:
                    print(f"  - 搜索失败: {str(e)}")
                    continue
        else:
            # 对于备用新闻源，直接调用
            try:
                news_items = source['function'](today)
                if news_items and len(news_items) > 0:
                    all_news.extend(news_items)
                    print(f"成功从{source['name']}获取{len(news_items)}条新闻")
            except Exception as e:
                print(f"从{source['name']}获取新闻失败: {str(e)}")
    
    # 翻译新闻标题
    print(f"开始翻译 {len(all_news)} 条新闻标题...") # 添加开始翻译的日志
    translated_news_count = 0
    processed_count = 0
    for news_item in all_news:
        processed_count += 1
        if processed_count % 10 == 0: # 每处理10条打印一次进度
            print(f"  已处理 {processed_count}/{len(all_news)} 条标题的翻译...")

        original_title = news_item.get('title')
        if original_title:
            translated_title = translate_text_to_chinese(original_title)
            if translated_title != original_title:
                news_item['title'] = translated_title
                news_item['original_title'] = original_title # 保留原始标题
                news_item['is_translated'] = True
                translated_news_count += 1
            else:
                news_item['is_translated'] = False
        else:
            news_item['is_translated'] = False # 确保即使没有标题也有这个字段
            print(f"  - 警告: 发现无标题新闻条目在翻译前: {news_item.get('link', '未知链接')}")

    print(f"所有标题翻译尝试完成。") # 添加结束翻译的日志
    if translated_news_count > 0:
        print(f"成功翻译 {translated_news_count} 条新闻标题。")
    else:
        print("没有新闻标题被翻译。")

    # 去重 (基于翻译后的标题)
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        # 确保 news['title'] 存在且不为空
        current_title = news.get('title')
        if current_title and current_title.strip() and current_title not in seen_titles:
            seen_titles.add(current_title)
            unique_news.append(news)
        elif not current_title or not current_title.strip():
            print(f"  - 警告: 发现空标题新闻，已跳过: {news.get('link', '未知链接')}")
    
    print(f"成功收集到{len(unique_news)}条独特的AI新闻")
    
    # 如果没有获取到任何新闻，返回备用新闻
    if not unique_news:
        print("所有在线新闻源都失败，使用本地备用新闻")
        return get_ai_news_from_alternative(today)
    
    return unique_news

def generate_html(news_items):
    """生成HTML页面展示新闻"""
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # 读取HTML模板
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 生成新闻项HTML
    news_html = ""
    for item in news_items:
        display_title = item.get('title', '无标题')
        if item.get('is_translated') and item.get('original_title'):
            # 如果标题被翻译了，可以在旁边显示原文或提示
            display_title += f" <span class='original-title-indicator'>(原文: {item['original_title'][:30]}...)</span>"
        
        news_html += f"""
        <div class="news-item">
            <h2><a href="{item.get('link', '#')}" target="_blank">{display_title}</a></h2>
            <p>{item.get('snippet', '无摘要')}</p>
        </div>
        """
    
    # 替换模板中的占位符
    html_content = template.replace('{{DATE}}', today).replace('{{NEWS_ITEMS}}', news_html)
    
    # 写入HTML文件
    with open('ai_news.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已生成AI新闻页面: ai_news.html")
    return os.path.abspath('ai_news.html')

def search_google(query):
    """从Google搜索获取AI新闻"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36', # 更新User-Agent
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7', # 添加Accept-Language
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' # 添加Accept
    }
    
    # 添加新闻标签以获取更相关的结果
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws&hl=en" # 添加hl=en指定英文结果，有时可避免地区限制
    
    try:
        # 增加超时时间和重试次数
        max_retries = 3 # 保持3次重试
        retry_delay = 5 # 初始延迟增加到5秒
        timeout_duration = 30 # 超时时间增加到30秒
        
        for attempt in range(max_retries):
            try:
                response = requests.get(search_url, headers=headers, timeout=timeout_duration)
                response.raise_for_status() # 如果状态码不是2xx，则抛出HTTPError异常
                break # 如果成功，跳出循环
            except requests.exceptions.Timeout as e:
                if attempt < max_retries - 1:
                    print(f"Google搜索超时 (尝试 {attempt+1}/{max_retries}): {str(e)}，等待 {retry_delay:.1f} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避，增加退避因子
                else:
                    print("Google搜索多次超时，请检查您的网络连接或尝试使用代理。")
                    return [] # 多次超时后返回空列表
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"Google连接错误 (尝试 {attempt+1}/{max_retries}): {str(e)}，等待 {retry_delay:.1f} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print("Google搜索连接错误，请检查您的网络连接。")
                    return []
            except requests.exceptions.HTTPError as e:
                # 特别处理429 Too Many Requests错误
                if response.status_code == 429:
                    print(f"Google搜索请求过于频繁 (状态码 429)，请稍后再试或减少请求频率。错误: {str(e)}")
                else:
                    print(f"Google搜索HTTP错误 (状态码 {response.status_code}): {str(e)}")
                return [] # HTTP错误直接返回空列表，不再重试
            except requests.exceptions.RequestException as e:
                # 捕获其他requests相关的异常
                if attempt < max_retries - 1:
                    print(f"Google搜索请求异常 (尝试 {attempt+1}/{max_retries}): {str(e)}，等待 {retry_delay:.1f} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Google搜索请求发生未知错误: {str(e)}。请检查网络或代理设置。")
                    return []
        else: # for循环正常结束 (没有break)，意味着所有重试都失败了
            if 'response' not in locals(): # 如果response变量未定义 (例如，所有尝试都超时)
                 print("Google搜索所有尝试均失败，未能获取响应。")
                 return []

        # 解析搜索结果
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # 更新选择器以适应可能的Google页面结构变化
        # 尝试多种常见的Google新闻结果选择器
        # Google经常更改其HTML结构，因此需要灵活的选择器
        # 常见的父容器可能是 'div.SoaBEf', 'div.g', 'div.Gx5Zad', 'div.WlydOe', 'div.xuvV6b'
        # 标题通常在 'div.mCBkyc', 'h3', 'div.n0jPhd', 'div.CEMjEf', 'div.GI74Re'
        # 链接通常在 'a'
        # 摘要通常在 'div.GI74Re', 'div.VwiC3b', 'div.st', 'div.yDYNvb', 'div.Y3v8qd'
        
        # 优先使用更具体的选择器组合
        results_container_selectors = ['div.SoaBEf', 'div.Gx5Zad', 'div.WlydOe', 'div.xuvV6b', 'div.g']
        title_selectors = ['div.n0jPhd span', 'div.mCBkyc', 'h3', 'div.CEMjEf span', 'div.GI74Re']
        link_selector = 'a'
        snippet_selectors = ['div.GI74Re', 'div.Y3v8qd', 'div.VwiC3b', 'div.st', 'div.yDYNvb']

        found_results = False
        for container_selector in results_container_selectors:
            for result_item_container in soup.select(container_selector):
                title = None
                link_element = result_item_container.select_one(link_selector)
                snippet = None

                for ts in title_selectors:
                    title_element = result_item_container.select_one(ts)
                    if title_element and title_element.text.strip():
                        title = title_element.text.strip()
                        break
                
                if not title and link_element: # 如果通过标准选择器找不到标题，尝试从链接文本获取
                    title = link_element.text.strip()

                for ss in snippet_selectors:
                    snippet_element = result_item_container.select_one(ss)
                    if snippet_element and snippet_element.text.strip():
                        snippet = snippet_element.text.strip()
                        break
                
                if title and link_element and link_element.get('href'):
                    raw_link = link_element.get('href')
                    # 清理Google重定向链接
                    if raw_link.startswith('/url?q='):
                        actual_link = raw_link.split('/url?q=')[1].split('&')[0]
                    elif raw_link.startswith('http'):
                        actual_link = raw_link
                    else:
                        actual_link = f"https://www.google.com{raw_link}" # 相对路径补全
                    
                    search_results.append({
                        'title': title,
                        'link': actual_link,
                        'snippet': snippet if snippet else "(无摘要)",
                        'source': 'Google'
                    })
                    found_results = True
            if found_results: # 如果在一个容器选择器中找到了结果，就跳出外层循环
                break
        
        if not search_results:
            print("未能从Google搜索结果中提取到新闻条目，可能是页面结构已更改或无相关结果。")

        return search_results

    except Exception as e:
        print(f"Google搜索过程中发生未预料的错误: {str(e)}")
        return []

def search_bing(query):
    """从Bing搜索获取AI新闻"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    search_url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
    
    try:
        # 添加超时设置和重试机制
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.get(search_url, headers=headers, timeout=15)
                break
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt < max_retries - 1:
                    print(f"尝试 {attempt+1}/{max_retries} 失败: {str(e)}，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # 指数退避
                else:
                    raise
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for item in soup.select('.news-card'):
                title_element = item.select_one('.title')
                source_element = item.select_one('.source')
                snippet_element = item.select_one('.snippet')
                link_element = item.select_one('a.title')
                
                if title_element and link_element:
                    title = title_element.text
                    link = link_element.get('href')
                    source = source_element.text.split('·')[0].strip() if source_element else "未知来源"
                    snippet = snippet_element.text if snippet_element else ""
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet,
                        'source': 'Bing'
                    })
            
            return results
        else:
            print(f"Bing搜索请求失败，状态码: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("Bing搜索请求超时，可能需要代理或网络连接有问题")
        return []
    except requests.exceptions.ConnectionError:
        print("Bing搜索连接错误，可能是网络问题或被限制访问")
        return []
    except Exception as e:
        print(f"Bing搜索过程中出错: {str(e)}")
        return []

def get_ai_news_from_alternative(today):
    """从备用新闻源获取AI新闻"""
    # 这里提供一些预设的AI新闻，作为网络连接失败时的备用
    # 实际应用中，可以替换为其他可靠的API或RSS源
    
    # 模拟从备用源获取的新闻
    current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
    alternative_news = [
        {
            'title': f"AI技术发展最新动态 - {current_date}",
            'link': "https://github.com/topics/artificial-intelligence",
            'snippet': "人工智能领域持续快速发展，各大科技公司推出新一代AI模型和应用。最新技术趋势包括多模态学习、自监督学习以及更高效的模型训练方法。",
            'source': '本地备用'
        },
        {
            'title': f"开源AI项目推荐 - {current_date}",
            'link': "https://github.com/topics/machine-learning",
            'snippet': "GitHub上热门的开源AI项目持续更新，包括自然语言处理、计算机视觉和强化学习等多个领域的创新工具和框架。",
            'source': '本地备用'
        },
        {
            'title': f"AI伦理与监管最新进展 - {current_date}",
            'link': "https://github.com/topics/ai-ethics",
            'snippet': "随着AI技术的广泛应用，伦理问题和监管框架受到越来越多关注。各国政府和组织正在制定相关政策，平衡技术创新与社会影响。",
            'source': '本地备用'
        },
        {
            'title': f"AI在医疗领域的应用进展 - {current_date}",
            'link': "https://github.com/topics/healthcare",
            'snippet': "人工智能在医疗诊断、药物研发和个性化治疗方面取得重要突破，提高医疗效率和准确性，为患者提供更好的医疗服务。",
            'source': '本地备用'
        },
        {
            'title': f"AI教育资源汇总 - {current_date}",
            'link': "https://github.com/topics/education",
            'snippet': "为学习人工智能提供的最新教育资源，包括在线课程、教程、书籍和实践项目，帮助初学者和专业人士提升AI技能。",
            'source': '本地备用'
        },
        {
            'title': f"AI与大数据分析最新趋势 - {current_date}",
            'link': "https://github.com/topics/data-science",
            'snippet': "人工智能与大数据分析技术的结合正在创造新的价值，企业通过AI驱动的数据分析获得更深入的业务洞察和决策支持。",
            'source': '本地备用'
        },
        {
            'title': f"AI在自然语言处理领域的突破 - {current_date}",
            'link': "https://github.com/topics/nlp",
            'snippet': "自然语言处理技术不断突破，大型语言模型在理解、生成和翻译人类语言方面表现出前所未有的能力，为各行业带来创新应用。",
            'source': '本地备用'
        },
        {
            'title': f"AI在计算机视觉领域的进展 - {current_date}",
            'link': "https://github.com/topics/computer-vision",
            'snippet': "计算机视觉技术持续发展，在图像识别、物体检测和场景理解等方面取得重要进展，为安防、自动驾驶等领域提供关键支持。",
            'source': '本地备用'
        }
    ]
    
    return alternative_news

def main():
    """主函数"""
    print("AI新闻聚合器启动...")
    
    try:
        # 搜集新闻
        news_items = search_ai_news()
        
        if news_items:
            print(f"成功获取 {len(news_items)} 条AI新闻")
            # 生成HTML页面
            html_path = generate_html(news_items)
            print(f"新闻页面已生成: {html_path}")
            print("请在浏览器中打开此文件查看今日AI新闻")
        else:
            print("未能获取任何AI新闻，请检查网络连接或稍后再试")
            print("您可以尝试README.md中的网络连接问题解决方案")
    except Exception as e:
        print(f"程序运行过程中发生错误: {str(e)}")
        print("使用备用新闻源...")
        try:
            # 使用备用新闻源
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            news_items = get_ai_news_from_alternative(today)
            if news_items:
                html_path = generate_html(news_items)
                print(f"已使用备用新闻生成页面: {html_path}")
                print("请在浏览器中打开此文件查看今日AI新闻")
        except Exception as inner_e:
            print(f"备用方案也失败了: {str(inner_e)}")
            print("请稍后再试或检查网络连接")

if __name__ == "__main__":
    main()