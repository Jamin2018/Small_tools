import requests
import bs4

# 获取单独的url
def movie_info(url):
    '''
    内容标签：<div id="Zoom">
    下载链接标签：--》a标签属性：thunderrestitle
    '''
    # url = 'http://www.dytt8.net/html/gndy/dyzz/20180118/56127.html'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                             "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        , 'Referer': 'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html', }


    html = requests.get(url, headers=headers)
    html.encoding = 'unicode'

    Soup = bs4.BeautifulSoup(html.content, 'html.parser')
    all_info = Soup.find('div', class_='co_content8').text

    title, movie_time, score, thunderrestitle = '', '', '', ''
    try:
        title = Soup.find('div', class_='bd3r').find('div', class_='co_area2').find('div', class_='title_all').text
    except:
        pass
    try:
        time_tag = all_info.index('发布时间')
        movie_time = all_info[time_tag:time_tag+15]
    except:
        pass
    try:
        score_tag = all_info.index('豆瓣评分')
        score = all_info[score_tag:score_tag + 12]
    except:
        pass
    try:
        thunderrestitle_tag = all_info.index('下载地址')
        try:
            thunderrestitle_tag_last = all_info.index('磁力链下载')
        except:
            thunderrestitle_tag_last = all_info.index('下载地址2')
        # thunderrestitle_tag_last = all_info.index('磁力链下载') if all_info.index('磁力链下载') else all_info.index('下载地址2')
        # thunderrestitle_tag_last = all_info.index('下载地址2')
        thunderrestitle = all_info[thunderrestitle_tag + 9:thunderrestitle_tag_last - 5]
    except:
        pass
    # print(title, movie_time, score, thunderrestitle)
    # print(all_info)
    # return {'title':title,'movie_time':movie_time,'score':score,'thunderrestitle':thunderrestitle}
    with open('电影天堂爬取下载链接.txt','a',encoding='utf8') as f:
        try:
            # f.write(str(title+movie_time+score+thunderrestitle))
            f.write(str(title + '/' + movie_time + '/' + score + thunderrestitle + '\n'))
        except:
            pass

    # print(all_info)


def get_url(page=2500):
    all_url = 'http://www.dytt8.net/html/gndy/dyzz/index.html'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                             "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        , 'Referer': 'http://www.dytt8.net/', }


    html = requests.get(all_url, headers=headers)
    html.encoding = 'unicode'

    Soup = bs4.BeautifulSoup(html.content, 'html.parser')
    all_info = Soup.find('select', attrs={"name":'sldd'}).findAll('option')
    urls = []

    n = 0
    for i in all_info:
        if n < page:
            # print(i.attrs['value'])
            url = 'http://www.dytt8.net/html/gndy/dyzz/' + i.attrs['value']
            # print(url)
            urls.append(url)
            n += 1
        else:
            break
    return urls


def get_movie_url(movie_url):
    # movie_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                             "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        , 'Referer': 'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html', }


    html = requests.get(movie_url, headers=headers)
    html.encoding = 'unicode'

    Soup = bs4.BeautifulSoup(html.content, 'html.parser')
    all_info = Soup.find('div', class_='co_content8').find('ul').findAll('table')

    movie_urls = []
    for i in all_info:
        url = 'http://www.dytt8.net' + i.find('a').attrs['href']
        print(i.find('a').attrs['href'])
        movie_urls.append(url)
    return movie_urls


# movie_info('http://www.dytt8.net/html/gndy/dyzz/20180121/56158.html')
if __name__ == '__main__':
    urls = get_url(1)
    for movie_url in urls:
        movie_urls = get_movie_url(movie_url)
        for url in movie_urls:
            movie_info(url)


# 下面这个页面爬取的是乱码，不知道为什么。
# url = 'http://www.dytt8.net/html/gndy/dyzz/20180130/56216.html'
#
# html = requests.get(url)
# html.encoding = 'unicode'
#
# Soup = bs4.BeautifulSoup(html.content, 'html.parser')
# all_info = Soup.find('div', class_='co_content8').text
# print(all_info)


