from pyecharts.charts import Bar, Funnel
from pyecharts import options as opts
import csv


# 柱状图
def emotion_bar(file_name):
    bar_x = []
    bar_y = []
    with open('draw/LDA词频.csv', encoding="utf-8") as csvfile:
        count = 0
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if count:
                bar_x.append(row[0])
                bar_y.append(row[1])
            count += 1

    # c = (Bar().add_xaxis(bar_x).add_yaxis(
    #     "回答数量", bar_y,
    #     color="#af00ff").set_global_opts(title_opts=opts.TitleOpts(
    #         title=file_name + "柱状图")).render("draw/" + file_name + "柱状图.html"))
    # print("绘制完成")

    bar_x = list(reversed(bar_x))
    bar_y = list(reversed(bar_y))

    bar = (Bar().add_xaxis(bar_x).add_yaxis(
        "", bar_y, stack="stack1").reversal_axis().set_global_opts(
            title_opts=opts.TitleOpts(title="LDA词频")).set_series_opts(
                label_opts=opts.LabelOpts(is_show=False, position="right")).
           render("draw/" + file_name + "柱状图.html"))


emotion_bar("LDA词频")
