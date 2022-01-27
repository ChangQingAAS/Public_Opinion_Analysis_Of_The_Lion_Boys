import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'  #设置中文显示
plt.figure(figsize=(6, 6))  #将画布设定为正方形，则绘制的饼图是正圆
label = ['百家号', '豆瓣影评', '知乎回答', 'b站', '知网文献']  #定义饼图的标签，标签是列表
values = [100, 4000, 10000, 40000, 10]
explode = [0.01, 0.01, 0.01, 0.01]  #设定各项距离圆心n个半径
#plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')  #绘制饼图
plt.title('数据量占比')  #绘制标题
# plt.savefig('./big_data/draw/数据量占比.png')  #保存图片
plt.show()