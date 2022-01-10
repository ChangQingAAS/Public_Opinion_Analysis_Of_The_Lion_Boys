from pyecharts.charts import Pie
from pyecharts import options as opts


# 用户情感可视化（饼状图）
def emotion_pie(file_name, positive_num, negative_num):
    bar_x_data = ("积极", "消极")
    bar_y_data = (positive_num, negative_num)
    c = (Pie(init_opts=opts.InitOpts(height="800px", width="1000px")).add(
        "情感分析概览", [list(z) for z in zip(bar_x_data, bar_y_data)],
        center=["35%", "38%"],
        radius="40%",
        label_opts=opts.LabelOpts(
            formatter="{b|{b}: }{c}  {per|{d}%}  ",
            rich={
                "b": {
                    "fontSize": 16,
                    "lineHeight": 33
                },
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            })).set_global_opts(
                title_opts=opts.TitleOpts(title=file_name + "情感分析饼状图", ),
                legend_opts=opts.LegendOpts(
                    pos_left="0%", pos_top="65%")).render("draw/" + file_name +
                                                          "情感分析饼状图.html"))
    print("情感分析饼状图绘制完成")


emotion_pie('知乎回答', 3294, 6712)
