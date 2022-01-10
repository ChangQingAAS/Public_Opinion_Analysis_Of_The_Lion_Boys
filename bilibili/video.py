# 爬视频信息
import time
import requests
import json
import pymysql  #
import multiprocessing
import traceback

# con = pymysql.connect(host='localhost',
#                       port=3306,
#                       user='root',
#                       passwd='1234',
#                       db='bili_info2')  # 密码和数据库名字啥的设自己的就行
# cursor = con.cursor()

# def saveData(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15,
#              d16):
#     global con, cursor
#     sql1 = "INSERT INTO video_info(aid,title,up_id,pubdate,duration,`view`,`like`,coin,star,`share`,dan,reply,his_rank,category,key_words)  VALUE('{}',\"{}\",'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\"{}\",\"{}\")".format(
#         d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15)
#     sql2 = "INSERT INTO up_info SET up_id= {},up_name= \"{}\"".format(d3, d16)
#     cursor.execute(sql1)
#     cursor.execute(sql2)
#     con.commit()

# def saveR(furl, error=1, said=0):  # 出错记录保存
#     global con, cursor
#     sql = "INSERT INTO record(url,error,aid) value('{}','{}','{}')".format(
#         furl, error, said)
#     cursor.execute(sql)
#     con.commit()


def timestamp_to_time(date):  # 把timestamp格式的时间转换为datetime格式
    timeStamp = date
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def find_dict(bb):
    rid_dict = {}
    for i in range(0, 2):
        time.sleep(1)  # 延时
        left = 0
        mid = 80000
        right = 160000
        p = mid
        for k in range(0, 50000):
            dis = right - left
            r = requests.get(
                'https://api.bilibili.com/x/web-interface/newlist?&rid={}&type=0&pn={}&ps=50&jsonp=jsonp'
                .format(bb[i], p))
            # r.encoding = r.apparent_encoding
            data = json.loads(r.text)
            # print(left, mid, right)
            if len(data['data']['archives']):
                right = right
                left = mid
                p = int((right + mid) / 2)
                mid = p
            else:
                left = left
                right = mid
                p = int((left + mid) / 2)
                mid = p
            if len(data['data']['archives']) and dis < 5:
                print('aid:{},页数:{},数量:{}'.format(bb[i], p, p * 50))
                break
        rid_dict[bb[i]] = p
    return rid_dict


def find_url(num):
    print('开始爬取页面数量')
    left = 0
    mid = 80000
    right = 160000  # 这三个数据定义的目的是
    p = mid
    for k in range(0, 50000):
        time.sleep(0.2)
        dis = right - left
        r = requests.get(
            'https://api.bilibili.com/x/web-interface/newlist?&rid={}&type=0&pn={}&ps=50&jsonp=jsonp'
            .format(num, p))
        # r.encoding = r.apparent_encoding
        data = json.loads(r.text)
        # print(left, mid, right)
        if len(data['data']['archives']):  # 判断第P页是否有数据
            right = right
            left = mid
            p = int((right + mid) / 2)
            mid = p
        else:
            left = left
            right = mid
            p = int((left + mid) / 2)
            mid = p
        if len(data['data']
               ['archives']) and dis < 2:  # 第P页有数据且“头尾”只差1，结束判断，得到页码
            print('aid:{},页数:{},数量:{}'.format(num, p, p * 50))
            break
    print('页面数量爬取结束')
    print('--开始生成URL池--')
    Url_Pool = []
    for m in range(0, p):
        url = "https://api.bilibili.com/x/web-interface/newlist?&rid={}&type=0&pn={}&ps=50&jsonp=jsonp".format(
            num, m)
        Url_Pool.append(url)
    print('--URL池生成结束--')
    return Url_Pool


def find_data(rid):
    aaa = {
        # 这里是一个字典，分类的rid和对应的页数
    }
    urlPool = find_url(rid)
    print(aaa[rid], len(urlPool))
    # noinspection PyBroadException
    try:
        for j in range(aaa[rid], len(urlPool)):
            # noinspection PyBroadException
            try:
                r = requests.get('{}'.format(urlPool[j]),
                                 timeout=500,
                                 headers=header)
                # r.encoding = r.apparent_encoding
                data = json.loads(r.text)
                if len(data['data']['archives']) != 0:
                    # noinspection PyBroadException
                    try:
                        for k in range(0, len(data['data']['archives'])):
                            # noinspection PyBroadException
                            try:
                                # noinspection PyBroadException
                                try:
                                    aid = data['data']['archives'][k]['aid']
                                    title = data['data']['archives'][k][
                                        'title'].replace('"',
                                                         '').replace("'", '')
                                    title = eval(repr(title).replace('\\', ''))
                                    duration = data['data']['archives'][k][
                                        'duration']
                                    up_id = data['data']['archives'][k][
                                        'owner']['mid']
                                    up_name = data['data']['archives'][k][
                                        'owner']['name']
                                    pubdate = data['data']['archives'][k][
                                        'pubdate']
                                    coin = data['data']['archives'][k]['stat'][
                                        'coin']
                                    dan = data['data']['archives'][k]['stat'][
                                        'danmaku']
                                    star = data['data']['archives'][k]['stat'][
                                        'favorite']
                                    his_rank = data['data']['archives'][k][
                                        'stat']['his_rank']
                                    like = data['data']['archives'][k]['stat'][
                                        'like']
                                    reply = data['data']['archives'][k][
                                        'stat']['reply']
                                    share = data['data']['archives'][k][
                                        'stat']['share']
                                    view = data['data']['archives'][k]['stat'][
                                        'view']
                                    category = data['data']['archives'][k][
                                        'tname']
                                    key_words = data['data']['archives'][k][
                                        'dynamic'].replace('"', '').replace(
                                            "'", '')
                                    print(aid, title, up_id, pubdate, duration,
                                          view, like, coin, star, share, dan,
                                          reply, his_rank, category, key_words,
                                          up_name)
                                    # saveData(aid, title, up_id, pubdate,
                                    #          duration, view, like, coin, star,
                                    #          share, dan, reply, his_rank,
                                    #          category, key_words, up_name)
                                    # print(aid, title, up_id, pubdate, duration, view, like, coin, star, share, dan, reply, his_rank, category, key_words, up_name)
                                    # saveR(urlPool[j][50:-18], 1, aid)
                                    print(urlPool[j][50:-18], 1, aid)

                                    print('\r爬取中', end="")
                                except Exception as e:
                                    if len(e.args) >= 2:
                                        if int(e.args[0]) == 1062:
                                            pass
                                        else:
                                            pass
                                    else:
                                        traceback.print_exc()
                                        aid = data['data']['archives'][k][
                                            'aid']
                                        title = 'error'
                                        title = eval(
                                            repr(title).replace('\\', ''))
                                        duration = data['data']['archives'][k][
                                            'duration']
                                        up_id = data['data']['archives'][k][
                                            'owner']['mid']
                                        up_name = data['data']['archives'][k][
                                            'owner']['name']
                                        pubdate = data['data']['archives'][k][
                                            'pubdate']
                                        coin = data['data']['archives'][k][
                                            'stat']['coin']
                                        dan = data['data']['archives'][k][
                                            'stat']['danmaku']
                                        star = data['data']['archives'][k][
                                            'stat']['favorite']
                                        his_rank = data['data']['archives'][k][
                                            'stat']['his_rank']
                                        like = data['data']['archives'][k][
                                            'stat']['like']
                                        reply = data['data']['archives'][k][
                                            'stat']['reply']
                                        share = data['data']['archives'][k][
                                            'stat']['share']
                                        view = data['data']['archives'][k][
                                            'stat']['view']
                                        category = data['data']['archives'][k][
                                            'tname']
                                        key_words = 'error'
                                        # saveData(aid, title, up_id, pubdate,
                                        #          duration, view, like, coin,
                                        #          star, share, dan, reply,
                                        #          his_rank, category, key_words,
                                        #          up_name)
                                        # saveR(urlPool[j][50:-18], -1, aid)
                                        print(aid, title, up_id, pubdate,
                                              duration, view, like, coin, star,
                                              share, dan, reply, his_rank,
                                              category, key_words, up_name)
                                        print(urlPool[j][50:-18], -1, aid)
                            except:
                                continue
                    except:
                        traceback.print_exc()
                        # saveR(urlPool[j][50:-18], -2)
                        print(urlPool[j][50:-18], -2)

                else:
                    return 0
            except:
                traceback.print_exc()
                # saveR(urlPool[j][50:-18], -3)  # -2代表爬取错误
                print(urlPool[j][50:-18], -3)  # -2代表爬取错误

            # saveR(urlPool[j][50:-18], 8)
            print(urlPool[j][50:-18], 8)
    except:
        traceback.print_exc()
        # saveR('error', -4)
        print('error', -4)


if __name__ == "__main__":
    aa = ['BV1dR4y1u7pv']  #他说这里应该是分类号，我当时把帖子关了，找不到了
    po = multiprocessing.Pool(4)
    for u in range(0, len(aa)):  # len(urlPool)
        po.apply_async(find_data, (aa[u], ))
    print("-----start-----")
    po.close()  # 关闭进程池，关闭后po不再接收新的请求
    po.join()  # 等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")