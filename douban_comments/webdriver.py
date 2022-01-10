# 需求：破解滑块验证码，完成登录

from selenium import webdriver
import time
# 导入动作链
from selenium.webdriver.common.action_chains import ActionChains

# 2. 调用浏览器
driver = webdriver.Chrome()

# 最大化窗口
driver.maximize_window()

# 3. 请求
driver.get(url='https://www.douban.com/')

# time.sleep(3)

# 1. 点击密码登录
# driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
# 出现问题：没有点击到密码登录，而是点击了电影
# 分析，可能的原因：
# 1. 页面没有加载完成就点击(不是因为这个)
# 2. xpath的路径指定到了电影，路径有问题（不是因为这个）
# 电影路径：//*[@id="anony-nav"]/div[1]/ul/li[2]
# 3. 是因为iframe标签：在主页面中嵌套一个子页面
# 解决：切入到子页面中
# switch_to.frame(0)   切入到iframe中
# 0代表第一个iframe标签
driver.switch_to.frame(0)
driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()

# 查找并输入账号
driver.find_element_by_id('username').send_keys('15222168550')
# 查找并输入密码
driver.find_element_by_id('password').send_keys('Why15222168550')
# 查找并点击登录
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]').click()

# 出现滑块验证码
# 移动滑块到指定位置，完成登录

time.sleep(3)

# 1. 获取滑块
# huakuai = driver.find_element_by_id('tcaptcha_drag_thumb')
# print(huakuai)
# 出现问题：没有找到元素
# 1. 可能是程序运行太快，滑块还没有加载完就开始查找，所以，休眠一会儿
# 2. id可能有问题
# 3. 可能是有iframe标签
# 切入到第2个iframe标签中
driver.switch_to.frame(1)
# 再查找滑块
huakuai = driver.find_element_by_id('tcaptcha_drag_thumb')

# 找到滑块后，需要按住并保持不动
# click_and_hold() 点击并保持点击状态
# on_element:将此状态加载到哪一个元素身上
# perform()：执行
ActionChains(driver).click_and_hold(on_element=huakuai).perform()

# 拖动滑块
# move_by_offset()  移动
# xoffset：横向移动距离，该网站每次滑动的距离差不多
# yoffset：纵向移动距离
ActionChains(driver).move_by_offset(xoffset=76, yoffset=0).perform()

# print(huakuai)

# 释放鼠标
# ActionChains(driver).release().perform()

# 出现问题：
# 网络恍惚了一下，请重试
# 原因：识别出是机器人了
# 需要将连续行的移动，转换成间断性的移动，完全模拟出人类的移动操作
# 先匀加速，再匀减速
# 涉及物理知识：a(加速度)


# 定义获取运动轨迹函数
def get_tracks(distance):
    """
    v = v0+at
    x = v0t+1/2at**2
    """
    # 定义存放运动轨迹的列表
    tracks = []
    # 定义初速度
    v = 0
    # 定义单位时间
    t = 0.5
    # 定义匀加速运动和匀减速运动的分界线
    mid = distance * 4 / 5
    # 定义当前位移
    current = 0
    # 为了一直移动，定义循环
    while current < distance:
        if mid > current:
            a = 2
        else:
            a = -3
        v0 = v
        # 计算位移
        x = v0 * t + 1 / 2 * a * t**2
        # 计算滑块当前位移
        current += x
        # 计算末速度
        v = v0 + a * t
        tracks.append(round(x))
    return tracks


tracks = get_tracks(176)
print(tracks)
for track in tracks:
    ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()

time.sleep(1)

# 释放鼠标
ActionChains(driver).release().perform()
