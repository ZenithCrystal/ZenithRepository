import os
import sys
import webbrowser

def main():
    """运行AI新闻收集器并自动打开生成的网页"""
    print("=== AI新闻聚合器 ===\n")
    print("1. 基础版 - 简单收集AI新闻")
    print("2. 高级版 - 多来源收集并分类AI新闻")
    
    choice = input("\n请选择要运行的版本 (1/2): ")
    
    if choice == "1":
        print("\n正在运行基础版AI新闻聚合器...\n")
        import ai_news_aggregator
        ai_news_aggregator.main()
    elif choice == "2":
        print("\n正在运行高级版AI新闻聚合器...\n")
        import advanced_ai_news_collector
        advanced_ai_news_collector.main()
    else:
        print("\n无效的选择，请输入1或2")
        return
    
    # 自动打开生成的HTML文件
    html_path = os.path.abspath('ai_news.html')
    if os.path.exists(html_path):
        print(f"\n正在打开新闻页面: {html_path}")
        webbrowser.open('file://' + html_path)
    else:
        print("\n未找到生成的HTML文件，请检查程序运行是否成功")

if __name__ == "__main__":
    main()