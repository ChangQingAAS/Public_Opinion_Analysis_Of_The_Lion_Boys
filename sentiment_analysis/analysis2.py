from aip import AipNlp
import pandas as pd


# 调用百度的ai接口进行情感分析
def isPostive(text):
    APP_ID = '24359968'
    API_KEY = '9SbGCCXdhu2GvEGo6WS3qVLV'
    SECRET_KEY = 'x9EUbsSkg9aX2bBlBdnDAU2Fl4RTAnAX'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    try:
        sentiment = client.sentimentClassify(text)['items'][0]['sentiment']
        if sentiment == 0:
            return "负向"
        elif sentiment == 1:
            return "中性"
        else:
            return "正向"
    except:
        return "中性"


if __name__ == '__main__':
    postive_num, middle_num, negative_num = 0, 0, 0
    with open('./sentiment_analysis/all.csv', encoding="utf-8") as f:
        items = f.readlines()
    for item in items:
        res = isPostive(item)
        if res == "正向":
            postive_num += 1
        elif res == "负向":
            negative_num += 1
        else:
            middle_num += 1
        print(negative_num, middle_num, postive_num)
