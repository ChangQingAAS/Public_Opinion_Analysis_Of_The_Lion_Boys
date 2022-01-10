import requests
import parsel
from lxml import etree
from config import headers
import re
import time


def get_work_href_included_id(work_name):

    url = 'https://www.douban.com/search?q=' + work_name
    # print("url is ", url)
    response = requests.get(url=url, headers=headers, timeout=100)
    print("response status when get_href ", response)

    res_html = etree.HTML(response.text)
    href_included_id_list = res_html.xpath(
        '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/@onclick'
    )[0]

    find_type = re.compile(r'dou_search_(.*?)\'', re.S)
    type = re.findall(find_type, href_included_id_list)[0]
    find_sid = re.compile(r'sid: (.*?),', re.S)
    sid = re.findall(find_sid, href_included_id_list)[0]

    if type == None:
        href_included_id = 'not found'
    else:
        href_included_id = 'https://' + type + '.douban.com/subject/' + sid

    # print('href_included_id is ', href_included_id)
    return href_included_id


def get_comments_list(work_href, work_name):
    if work_href != 'not found':
        page_count = 0
        for page in range(181, 401, 20):
            page_count += 1
            print(
                f'-------------------正在爬取第{page_count}页的数据--------------------'
            )
            url = f'{work_href}/comments?start={page}&limit=20&status=P&sort=new_score'
            time.sleep(100)
            response = requests.get(url=url, headers=headers, timeout=100)
            print("response status when get_comments ", response)
            html_data = response.text
            print("html_data is ", html_data)

            selector = parsel.Selector(
                html_data)  # 转换数据类型 -->xpath 过时：lxml bs4
            comments_list = selector.xpath(
                '//span[@class="short"]/text()').getall()  # getall()取数据

            with open('./douban_comments/comments/' + work_name + '_短评.txt',
                      mode='a+',
                      encoding='utf-8') as f:

                for comment in comments_list:
                    # print(comment)
                    f.write(comment.replace('\n', ''))
                    f.write('\n')
                    f.write('\n')
        return comments_list
    else:
        with open('./douban_comments/comments/' + work_name + '_短评.txt',
                  mode='a+',
                  encoding='utf-8') as f:
            f.write('NOT FOUND')
        return ['not found']