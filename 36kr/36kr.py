import urllib.request
from bs4 import BeautifulSoup
import pip._vendor.html5lib.filters.inject_meta_charset
import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

baseUrl = 'https://36kr.com/newsflashes'


def getHtml(url):
    try:
        data = urllib.request.urlopen(url)
        html = data.read()
    except Exception as err:
        print('error:', err)
        html = 'error'
    return html


def getDocument(html, dtype, attr):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        ps = soup.find_all(dtype, attrs=attr)
    except Exception:
        ps = []
    return ps


def GetWeekday():
    weekday = datetime.datetime.now().weekday()
    if weekday == 0:
        return '星期一'
    elif weekday == 1:
        return '星期二'
    elif weekday == 2:
        return '星期三'
    elif weekday == 3:
        return '星期四'
    elif weekday == 4:
        return '星期五'
    elif weekday == 5:
        return '星期六'
    elif weekday == 6:
        return '星期日'


if __name__ == '__main__':
    html = getHtml(baseUrl)
    index = 1
    ps = getDocument(html, 'a', {'class': 'item-title'})
    date = datetime.datetime.now()
    # print(str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日' + GetWeekday() + ',' + '每日科技快讯：')
    text = str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日' + GetWeekday() + ',' + '每日科技快讯：'+ '\\n> '
    for p in ps:
        text += str(index) + '.' + p.text +'\\n '
        # print(text)
        index += 1
    print(text)