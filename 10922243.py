import feedparser
import pandas as pd

def fetch_rss_titles(url):
    # 使用feedparser解析RSS資料
    feed = feedparser.parse(url)

    # 檢查是否成功取得RSS資料
    if feed.get('bozo_exception'):
        print(f"Error fetching RSS feed: {feed.bozo_exception}")
        return

    # 找出含有「台中」的標題
    taipei_titles = [entry.title for entry in feed.entries if '台中' in entry.title]

    # 列印含有「台中」的標題
    print("Titles with 台中:")
    for title in taipei_titles:
        print(title)

    # 如果有找到含有「台中」的標題，則保存至 Excel 檔案
    if taipei_titles:
        df = pd.DataFrame({'Title': taipei_titles})
        df.to_excel('taipei_titles.xlsx', index=False)
        print("Titles with 台中 saved to taipei_titles.xlsx")

if __name__ == "__main__":
    # 設定RSS網址
    url = "https://news.pts.org.tw/xml/newsfeed.xml"

    # 呼叫函式取得標題並列印
    fetch_rss_titles(url)

