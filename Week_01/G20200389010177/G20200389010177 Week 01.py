import requests
from lxml import etree
import re
import time
import csv


# 参数设置
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
}

# 获取电影榜单
def get_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    movies = selector.xpath('//div[@class="info"]')
    for movie in movies:
        title = movie.xpath('div[@class="hd"]/a/span[1]/text()')[0]
        rating_num = movie.xpath('div[@class="bd"]/div[@class="star"]/span[2]/text()')[0]
        movie_link = movie.xpath('div[@class="hd"]/a/@href')[0]
        rating_num, quote1, quote2, quote3, quote4, quote5 = get_movie_quote(movie_link)
        alist=[title, rating_num, quote1, quote2, quote3, quote4, quote5]
        print(alist)
        time.sleep(1)
        writer.writerow((title, rating_num, quote1, quote2, quote3, quote4, quote5))


# 获取电影评价人数及短评
def get_movie_quote(movive_link):
    index_pattern = re.compile(r'https://movie.douban.com/subject/(\d+)/')
    movie_index = index_pattern.findall(movive_link)[0]
    quote_url = f'https://movie.douban.com/subject/{movie_index}/comments?sort=new_score&status=P'
    res = requests.get(quote_url, headers=headers)
    selector = etree.HTML(res.text)

    # 获取5条热门短评
    quote1 = selector.xpath('//*[@id="comments"]/div[1]/div[2]/p/span/text()')[0]
    quote2 = selector.xpath('//*[@id="comments"]/div[2]/div[2]/p/span/text()')[0]
    quote3 = selector.xpath('//*[@id="comments"]/div[3]/div[2]/p/span/text()')[0]
    quote4 = selector.xpath('//*[@id="comments"]/div[4]/div[2]/p/span/text()')[0]
    quote5 = selector.xpath('//*[@id="comments"]/div[5]/div[2]/p/span/text()')[0]
    rating_num = selector.xpath('//*[@id="content"]/div/div[1]/div[1]/ul/li[1]/span/text()')[0]

    # 获取评价人数
    number_pattern = re.compile('.*?(\d+)')
    number = number_pattern.findall(rating_num)[0]
    return number, quote1, quote2, quote3, quote4, quote5


# 以UTF-8保存到csv格式中
with open('book_top250000.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('电影名称', '评价人数', '短评1', '短评2', '短评3', '短评4', '短评5'))

    urls = list(f'https://movie.douban.com/top250?start={i * 25}&filter=' for i in range(0, 1))
    for url in urls:
        get_info(url)
        time.sleep(5)
