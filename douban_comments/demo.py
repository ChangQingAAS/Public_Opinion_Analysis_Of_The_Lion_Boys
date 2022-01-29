import requests
import json
import re
import os
import pandas as pd
import time
from bs4 import BeautifulSoup


def Agent_info():
    """用于保存Cookies、Url、user-agent、headers信息等"""

    headers = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67",
        "Cookie":
    }

    return headers


def get_html(url):
    """获取网页全部数据"""

    headers = Agent_info()
    try:
        r = requests.get(url=url, headers=headers, timeout=100)
        r.encoding = r.apparent_encoding
        status = r.status_code  # 爬虫的状态

        datas = json.loads(r.text)["html"]
        str_html = "<html>{}</html>".format(datas)
        # 注意：.prettify()会将数据格式转换为 str 格式，所以这里放弃格式化标签处理
        html = BeautifulSoup(str_html, "html.parser")

        print("爬虫状态码: " + str(status))
        # print(type(html))
        # 此时返回的是一个 html标签的全部内容，且经过格式化处理(str格式)
        return html
    except Exception as e:
        print("很遗憾，数据爬取失败！")
        print(e)


def etl_data(html):
    """提取出我们想要的数据"""

    # 将所有用户的评论单独存放在列表, .find_all方法需要数据为<class 'bs4.BeautifulSoup'>格式
    comments = html.find_all('div', 'comment-item')
    # print(comments[0])

    # 获取电影的评论并保存到列表（时间，用户，星级，短评，支持数）
    datas = []

    for span in comments:
        # 短评发表的时间
        times = span.find('span', 'comment-time').attrs['title']
        # 用户名
        name = span.find('a').attrs["title"]
        # 用户评分星级
        # 可用.attrs['class'][0][-2:]获取星级（为末尾的两位数，）
        try:
            level = span.find('span', 'rating').attrs['class'][0][-2:]
            if (level == '10'):
                level = "一星"
            elif (level == '20'):
                level = "二星"
            elif (level == '30'):
                level = "三星"
            elif (level == '40'):
                level = "四星"
            elif (level == '50'):
                level = "五星"
        except Exception as e:
            # 因为会存在有用户写评价但是不打星级的情况
            level = "无评价"

        # 短评, .strip()去出评论两端的换行符
        content = span.find('span', 'short').string.strip()
        # 将评论中存在的换行符删除（替换为无空格符）
        content = re.sub(r'\n', '', content)

        # 短评支持数
        love_point = span.find('span', 'vote-count').string.strip()

        arr = [times, name, level, content, love_point]
        datas.append(arr)

        df = pd.DataFrame(datas)
        df.columns = ["时间", "用户", "星级", "短评", "支持数"]

        # print(arr)
    return df


def get_nextUrl(html):
    """抓取下一个页面的 url"""

    try:
        # 找到下一页的 url
        url = html.find('a', 'next').attrs['href']
        # print(url)
        next_start = re.search(r'[0-9]\d{0,5}', url).group(0)
        print("已经到 " + str(next_start) + " 了哦~, 客官稍等一会儿\n")

        next_url = "https://movie.douban.com/subject/35144311/comments?percent_type=" \
                   "&start={}&limit=20&status=P&sort=new_score&comments_only=1&ck=Cuyu".format(next_start)
        # print(next_url)

        return next_url
    except:
        print("客官，已经没有短评数据了~ 欢迎下次再来哦~")


def save_data(data, fileName, Flag):
    """持久化存储数据"""

    file_name = fileName + "_" + time.strftime(
        "%Y_%m_%d", time.localtime(time.time())) + ".csv"
    # print(file_name)

    # 存储为csv格式文件
    data.to_csv(file_name,
                index=False,
                header=Flag,
                mode='a',
                encoding="utf_8_sig")

    # 检查是否保存成功，并打印提示文本
    if os.path.exists(file_name):
        print(file_name + " 数据爬取并保存成功！")
    else:
        print('数据保存失败,请再次尝试！')


if __name__ == "__main__":
    """程序入口"""

    # 将要访问的Url
    url = "https://movie.douban.com/subject/35144311/comments?percent_type=" \
          "&start={}&limit=20&status=P&sort=new_score&comments_only=1&ck=Cuyu".format(0)

    # 1.获取网页数据
    html = get_html(url)

    # 2.抽取数据（时间，用户，星级，短评，支持数）
    data = etl_data(html)

    # 3.保存首页的数据
    fileName = input("请输入保存文件的名字:")
    save_data(data, fileName, True)

    # 3.获取下一个访问链接
    next_url = get_nextUrl(html)

    isFlag = True
    while (next_url):
        try:
            next_html = get_html(next_url)
            next_data = etl_data(next_html)
            save_data(next_data, fileName, False)
            next_url = get_nextUrl(next_html)
        except:
            break
