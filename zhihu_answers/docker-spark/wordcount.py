import jieba

# 读取数据
text = open('/usr/local/l.csv', 'r', encoding="utf-8").read()
len(text)

# 全部字符变成小写字符
text = text.lower()

# 读取停用词，创建停用词表
stwlist = [
    line.strip()
    for line in open('/usr/local/cn_stopwords.txt', 'r', encoding="utf-8").readlines()
]

# 先进行分词
words = jieba.cut(text, cut_all=False, HMM=True)
# cut_all:是否采用全模式
# HMM：是否采用HMM模型

# 去停用词,统计词频
word_ = {}
for word in words:
    if word.strip() not in stwlist:
        if len(word) > 1:
            if word != '\t':
                if word != '\r\n':
                    #计算词频
                    if word in word_:
                        word_[word] += 1
                    else:
                        word_[word] = 1

# 将词汇和词频以元组的形式保存
word_freq = []
for word, freq in word_.items():
    word_freq.append((word, freq))

# 进行降序排列
word_freq.sort(key=lambda x: x[1], reverse=True)

# 查看前200个结果
# for i in range(20):
#     word, freq = word_freq[i]
#     print(word, freq)

#将结果保存
with open('/usr/local/result.txt', 'w', encoding="utf-8") as f:
    for word, freq in word_freq:
       f.write('%s,%d\n' % (word, freq))
