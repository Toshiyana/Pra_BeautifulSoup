import time
import urllib.request
from bs4 import BeautifulSoup

# サーバにアクセス毎にプログラムが停止する時間（秒）
DELTA = 2

# htmlを取得する関数
def get_html(url):
    html = urllib.request.urlopen(url).read()
    time.sleep(DELTA)
    return html

# 東京のリスト（鉄道会社名、路線）を返す関数
def get_lines():
    url = 'https://transit.yahoo.co.jp/station/list?pref=13&prefname=%E6%9D%B1%E4%BA%AC&done=sta'
    html = get_html(url)

    # BeautifulSoup
    # 取得したhtmlからBeautifulSoupインスタンスを作成（目的のページのhtml構造が分かれば、データの抽出可能）
    # soup = BeautifulSoup(html, features='lxml')# purePythonで書かれている（pipいらない）
    soup = BeautifulSoup(html, features='lxml')# Cythonで書かれている (pip install lxml 必要)。lxmlの方が速いらしい。
    # urlタグのBeautifulSoupインスタンスを取得
    info = soup.find('ul', {'class': 'elmSearchItem line'})

    # (鉄道会社名、路線名のタプルのリスト)
    company_line = []
    for group in info.find_all('dl'): # find_all: 合致する全てのタグのインスタンスをreturn
        company = group.find('dt').get_text()
        line_tags = group.find_all('a')
        for li in line_tags:
            line = li.get_text()# 線路名の取得
            company_line.append((company, line))

    return company_line


if __name__ == '__main__':
    print(get_lines())