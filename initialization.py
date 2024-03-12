'''
由于青马课程需要先进入视频一次页之后才会在个人中心的对应位置显示，
所以先进入个人中心检测各个类型课程数量是否存在小于10的,如果有，则进入首页点击一下视频一次
'''
# 本模块用于初始化，检测是否需要进入视频一次页以及进行进入视频一次页操作

from DrissionPage import ChromiumPage
from DrissionPage.common import *
import json
import time
from loguru import logger
from get_info import get_info
from collections import *
from get_info import login

def click_videoes(study_type:str) -> None:
    '''
    study_type:只能在如下选项中选择
    1、入党积极分子
    2、网络文明志愿者
    3、团学干部
    4、大学生心理健康教育
    '''
    # 由于各位学员的培训种类不同，这里交给用户输入

    # 必修，选修，专栏学习是每人都要学习的，统一处理
    def must_study():
        pass
    def elective_study():
        pass
    def column_study():
        pass


# 读取课程数量信息
def init():
    '''
    初始化，检测是否需要进入视频一次页以及进行进入视频一次页操作
    '''
    # 获取课程数量信息
    get_info()
    class_info = json.load(open('course_info.json','r'))
    # 读取各个类别的课程数量
    cnt = Counter(class_info[k]['type'] for k in class_info.keys())
    # 检测是否存在小于10的课程数量
    less_10 = [k for k, v in cnt.items() if v < 10]
    if not less_10:
        # 直接进行刷课和检测
        return
    else:
        '''
        回到首页,逐个点击相应视频,每个视频页面停留3秒后推出,并进入下一个视频。
        结束调用get_info()函数，更新课程数量信息
        '''
        # 接管当前页面
        page = ChromiumPage()
        # 进入青马课堂页
        login(first=True,init=True)
        page.ele('tag:a@@text():青马课堂').hover()
        page.ele('tag:a@@text():全部').click().for_new_tab()
    click_videoes()