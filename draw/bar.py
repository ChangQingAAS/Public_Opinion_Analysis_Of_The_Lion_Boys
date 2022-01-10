from pyecharts.charts import Bar
from pyecharts import options as opts


# 用户情感可视化（柱状图）
def emotion_bar(file_name):
    bar_x_data = ("主题0", "主题1", "主题2", "主题3", "主题4")
    bar_y_data = (1068, 4227, 412, 2213, 1777)
    c = (Bar().add_xaxis(bar_x_data).add_yaxis(
        "回答数量", bar_y_data,
        color="#af00ff").set_global_opts(title_opts=opts.TitleOpts(
            title=file_name + "柱状图")).render("draw/" + file_name + "柱状图.html"))
    print("情感分析柱状图绘制完成")


emotion_bar("知乎回答LDA主题")