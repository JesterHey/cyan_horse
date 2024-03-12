'''
由于青马课程需要先进入视频一次页之后才会在个人中心的对应位置显示，
所以先进入个人中心检测各个类型课程数量是否存在小于10的,如果有，则进入首页点击一下视频一次
'''
# 本模块用于初始化，检测是否需要进入视频一次页以及进行进入视频一次页操作

from DrissionPage import ChromiumPage
from DrissionPage.common import *
import json
import time
from logru import logger
from get_info import get_info
from collections import *

# 读取课程数量信息
get_info()
class_info = json.load(open('course_info.json','r'))
# 读取各个类别的课程数量
cnt = Counter(class_info[k]['type'] for k in class_info.keys())
# 检测是否存在小于10的课程数量
less_10 = [k for k, v in cnt.items() if v < 10]