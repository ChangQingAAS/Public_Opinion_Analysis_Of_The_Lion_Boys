from make_pic import make_wordcloud_pic
from spider import get_work_href_included_id, get_comments_list


# 输入对于当前work_name的特殊停用词
def input_stopwords(stopwords):
    # this_current_stopwords = set()
    # flag = True
    # while flag:
    #     item = input('请输入词云屏蔽词，否则输入q：')
    #     if item == 'q':
    #         flag = False
    #     else:
    #         this_current_stopwords.add(item)
    this_current_stopwords = stopwords
    return this_current_stopwords


if __name__ == '__main__':
    # 定义一些全局变量
    current_stopwords = set()
    work_name = input('请输入你想搜索的书籍或电影或音乐：')
    # work_name = str(work_name)
    work_href = get_work_href_included_id(work_name)
    work_comments_list = get_comments_list(work_href, work_name)
    make_wordcloud_pic(work_comments_list, work_name, current_stopwords)
