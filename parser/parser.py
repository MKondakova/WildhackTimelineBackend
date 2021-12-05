import requests
from bs4 import BeautifulSoup

HEADERS={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
         'accept':'*/*'}
HOST1='https://kamchatinfo.com'
HOST2='https://kamtoday.ru'

def get_html(url,params):
    return requests.get(url,headers=HEADERS,params=params)

def get_pages_count(html):
    soup=BeautifulSoup(html,'html.parser')
    pagination= soup.find_all(id='pages')
    if pagination:
        return int(((pagination[-1]).get_text()).split()[-1])
    else:
        return 1

def get_conent(html,n):
    soup=BeautifulSoup(html,'html.parser')
    if n==1:
        items=soup.find_all(class_="ns")
    if n==2:
        items=soup.find_all(class_="col-md-4")
        items2 = soup.find_all(class_="col-lg-3 col-sm-6")
    if n==3:
        items=soup.find_all(class_="search-item")
    news=[]
    for item in items:
        if n==1:
            news.append({
                'title': item.find('h3').get_text(),
                'data': item.find('h5').get_text(),
                # 'text': item.find(class_="tx").get_text(),
                'href': HOST1 + item.find('h3').find('a').get('href')
            })

        if n==2:
            news.append({
                'title': item.find(class_='name').get_text(),
                'data': item.find('span',class_="date darkgray").get_text(),
                'href': HOST2+item.find(class_='name').get('href')
            })
        if n==3:
            news.append({
                'title': item.find('h3').get_text(),
                'data': item.find(class_='search-item-date').find('span').get_text(),
                'href': HOST1 + item.find('h3').find('a').get('href')
            })

    if n==2:
        for item in items2:
            news.append({
                'title': item.find(class_='name').get_text(),
                'data': item.find('span', class_="date darkgray").get_text(),
                # 'text': item.find(class_="tx").get_text(),
                'href': HOST2 + item.find(class_='name').get('href')
            })
    print(news)
    return news

def parse(url,n):
    html=get_html(url,None)
    if html.status_code==200:
        news=[]
        pages_count=get_pages_count(html.text)
        if n==2:
            pages_count=85
        if n==3:
            pages_count=6

        for page in range(2, pages_count+1) :
            if n == 1:
                if page==1: html = get_html(url, {'page': page})
                else: html = get_html(url+'page/'+str(page)+'/',None)
            if n == 2 or n==3: html = get_html(url, {'PAGEN_1': page})
            news.extend(get_conent(html.text,n))
        return(news)
    else:
        print('error')
        return []


news=[]

news.extend(parse('https://kamchatinfo.com/news/ecology/',1))

news.extend(parse('https://kamtoday.ru/news/ecologics/',2))

news.extend(parse('https://poluostrov-kamchatka.ru/pknews/search/?tags=%D1%8D%D0%BA%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F',3))

print(news)