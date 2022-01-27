from pyecharts.charts import Pie
from pyecharts import options as opts
import numpy as np

# 导入玫瑰图所需颜色
color_series = [
    '#FAE927',
    '#9ECB3C',
    '#3DBA78',
    '#2B55A1',
    '#A63F98',
    '#D5225B',
]

# 实例化Pie类
pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# 设置颜色
pie1.set_colors(color_series)

bar_x_data = ['推荐', '力荐', '还行', '较差', '很差']
bar_y_data = [46.2, 36.8, 13.6, 1.9, 1.5]

# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie1.add("", [list(z) for z in zip(bar_x_data, bar_y_data)],
         radius=["20%", "100%"],
         center=["30%", "65%"],
         rosetype="area")  #将人数d取平方根，并且再四舍五入，注意都要有np导入

pie1.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
# 设置系列配置项
pie1.set_series_opts(label_opts=opts.LabelOpts(
    is_show=True,
    position="inside",
    font_size=12,
    formatter="{b}:{c}%",
    font_style="italic",
    font_weight="bold",
    font_family="Microsoft YaHei"), )
# 生成html文档
pie1.render('./draw/豆瓣评分_.html')
