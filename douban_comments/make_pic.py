import jieba
import wordcloud
import imageio
import mplcyberpunk
import matplotlib.pyplot as plt


# 制作词云图
def make_wordcloud_pic(comments_list, work_name, current_stopwords):

    with open('./douban_comments/comments/' + work_name + '_短评.txt',
              mode='r',
              encoding='utf-8') as f:
        txt = f.read()

    if txt == 'not found':
        txt_list_to_string = 'not found'
    else:
        # 中文分词
        txt_list = jieba.lcut(txt)
        # print('中文分词后的结果', txt_list)
        """
        这里join的参数为一个空格，则输出词云图中只有词语。
        若参数为空，则输出词云图有词和句子（但是句子有重复的
        """
        txt_list_to_string = ' '.join(txt_list)
        # print('合并之后的字符串', txt_list_to_string)

    # 词云图的轮廓
    img = imageio.imread('./douban_comments/outline/pp.png')
    """
    如果不扣图的话就不会识别轮廓，整张图片都是词云
    如果扣的话，词语就会按扣除的轮廓排布
    """

    wc = wordcloud.WordCloud(
        # 长宽可以自己想办法从图片提取吗
        # width=400,
        # height=200,
        background_color='black',
        font_path='msyh.ttc',  # 微软雅黑（系统自带
        mask=img,  # 词云图所用的图片
        scale=10,  # 字体大小 
        stopwords=set([
            line.strip()
            for line in open('./douban_comments/stop_words/cn_stopwords.txt',
                             mode='r',
                             encoding='utf-8').readlines()
        ]) | current_stopwords  # 停用词即没用的（虚词等）
    )

    # 给词云图输入文字
    wc.generate(txt_list_to_string)

    # 添加赛博朋克风格
    plt.style.use("cyberpunk")
    mplcyberpunk.add_glow_effects()

    # 保存云图
    wc.to_file('./douban_comments/comments/' + work_name + '_短评_词云.png')
    return 0