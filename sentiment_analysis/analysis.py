from aip import AipNlp
import pandas as pd


# 调用百度的ai接口进行情感分析
def isPostive(text):
    APP_ID = '24359968'
    API_KEY = '9SbGCCXdhu2GvEGo6WS3qVLV'
    SECRET_KEY = 'x9EUbsSkg9aX2bBlBdnDAU2Fl4RTAnAX'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    try:
        if client.sentimentClassify(text)['items'][0]['positive_prob'] > 0.5:
            return "积极"
        else:
            return "消极"
    except:
        return "积极"


if __name__ == '__main__':
    postive_num, negative_num = 0, 0
    with open('./all.csv', encoding="utf-8") as f:
        items = f.readlines()
    for item in items:
        print(item)
        if isPostive(item) == "积极":
            postive_num += 1
        else:
            negative_num += 1
        print(postive_num, negative_num)
