from gensim import corpora, models
import jieba.posseg as jp, jieba
import csv
import numpy

number_topics = 5

# 文本集
texts = []
with open("./TF-IDF/all.csv", 'r', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            texts.append(row[0])
        except:
            # print(row)
            pass

# print(len(texts))

# 停词表
stopwords = set([
    line.strip() for line in open(
        './TF-IDF/cn_stopwords.txt', mode='r', encoding='utf-8').readlines()
])

# 分词过滤条件
flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性

# 分词
words_ls = []
for text in texts:
    words = [
        w.word for w in jp.cut(text)
        if w.flag in flags and w.word not in stopwords
    ]
    words_ls.append(words)
# print(words_ls)

# 构造词典
dictionary = corpora.Dictionary(words_ls)
# 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
corpus = [dictionary.doc2bow(words) for words in words_ls]
# lda模型，num_topics设置主题的个数
lda = models.ldamodel.LdaModel(corpus=corpus,
                               id2word=dictionary,
                               num_topics=number_topics)

with open("./TF-IDF/result.txt", 'w+', encoding="utf-8") as f:
    # 打印所有主题，每个主题显示20个词
    for topic in lda.print_topics(num_words=15):
        print(topic)
        # topic = str(topic).rstrip(")").lstrip("(")
        topic = str(topic)
        f.write(topic + "\n")

topic_counter = [0 for i in range(number_topics)]

for count, values in enumerate(lda.inference(corpus)[0]):
    max_value = max(values)
    max_index = numpy.where(values == max_value)[0][0]
    topic_counter[max_index] += 1
    # print("第%d条数据的主题为%d, 值是%s" % (count + 1, max_index, max_value))

for number, topic in enumerate(topic_counter):
    print("属于第%d个主题的数据有%d条" % (number, topic))
