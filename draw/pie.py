from pyecharts.charts import Pie
from pyecharts import options as opts


def emotion_pie(file_name):
    # bar_x_data = ('5星', '4星', '3星', '2星', '1星')
    bar_x_data = ('力荐', '推荐', '还行', '较差', '很差')
    bar_y_data = (36.8, 46.2, 13.6, 1.9, 1.5)
    c = (
        Pie(init_opts=opts.InitOpts(height="700px", width="900px")).add(
            "情感分析概览",
            [list(z) for z in zip(bar_x_data, bar_y_data)],
            center=["25%", "35%"],
            radius="40%",
            label_opts=opts.LabelOpts(
                # formatter="{b|{b}: }{c}  {per|{d}%}  ",
                formatter="{b|{b}: }  {per|{d}%}  ",
                rich={
                    "b": {
                        "fontSize": 16,
                        "lineHeight": 33
                    },
                    # "per": {
                    #     "color": "#eee",
                    #     "backgroundColor": "#334455",
                    #     "padding": [2, 4],
                    #     "borderRadius": 2,
                    # },
                })).set_global_opts(
                    title_opts=opts.TitleOpts(title=file_name + "豆瓣短评评分占比", ),
                    legend_opts=opts.LegendOpts(
                        pos_left="0%",
                        pos_top="50%")).render("draw/" + file_name +
                                               "豆瓣评分.html"))

emotion_pie('')
