import os
from importlib import reload
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from gensim import corpora, similarities, models
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import jieba.posseg as pseg
import matplotlib.pyplot as plt
from gensim.models import CoherenceModel
from LDA import infile, deal, run, save_visual


#超参搜索的形式探索最佳主题数,对于暴力搜索可以一开始设置区间较大，步伐较大，目的是锁定大致区间范围，而后在小区间范围内精细化搜索。
def compute_coherence_values(dictionary, corpus, texts, start, limit, step):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    perplexs = []
    model_list = []
    for num_topic in range(start, limit, step):
        #模型
        lda_model, coherence_lda, perplex = run(corpus, dictionary, num_topic,
                                                texts)
        #lda_model = LdaModel(corpus=corpus,num_topics=num_topic,id2word=dictionary,passes=50)
        model_list.append(lda_model)
        perplexs.append(perplex)  #困惑度
        #一致性
        #coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        #coherence_lda = coherence_model_lda.get_coherence()
        coherence_values.append(coherence_lda)

    return model_list, coherence_values, perplexs


def show_1(dictionary, corpus, texts, start, limit, step):
    #从 5 个主题到 30 个主题，步长为 5 逐次计算一致性，识别最佳主题数
    model_list, coherence_values, perplexs = compute_coherence_values(
        dictionary, corpus, texts, start, limit, step)
    #输出一致性结果
    n = 0
    for m, cv in zip(perplexs, coherence_values):
        print("主题模型序号数", n, "主题数目", (n + 4), "困惑度", round(m, 4), " 主题一致性",
              round(cv, 4))
        n = n + 1
    #打印折线图
    x = list(range(start, limit, step))
    #困惑度
    plt.plot(x, perplexs)
    plt.xlabel("Num Topics")
    plt.ylabel("perplex  score")
    plt.legend(("perplexs"), loc='best')
    plt.show()
    #一致性
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

    return model_list


def choose(model_list, n):
    # 选择最佳主题并输出，一致性最高的
    optimal_model = model_list[n]
    model_topics = optimal_model.show_topics(formatted=False)
    #print(model_topics)
    return optimal_model


if __name__ == '__main__':
    train = infile(
        r'C:\Users\admin\Desktop\big_data\LDA\all.csv'
    )
    id2word, texts, corpus = deal(train)
    model_list = show_1(id2word, corpus, texts, 4, 16,
                        1)  #找出困惑度和主题一致性最佳的，最好是不超过20个主题数,10个为宜
    n = input('输入指定模型序号，以0为第一个: ')  # 还是需要手动，权衡比较
    optimal_model = choose(model_list, int(n))
    #主题列表
    topic_list = optimal_model.print_topics()
    #保存主题
    with open('all_result.txt', 'w', encoding='utf-8') as f:
        for t in topic_list:
            f.write(' '.join(str(s) for s in t) + '\n')
