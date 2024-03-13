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


def click_videoes(study_type: str, class_info: dict) -> None:
    '''
    study_type:只能在如下选项中选择
    1、入党积极分子
    2、网络文明志愿者
    3、团学干部
    4、大学生心理健康教育
    '''
    click_page = ChromiumPage()  # 接管当前页面
    valid_type = ['入党积极分子', '网络文明志愿者', '团学干部', '大学生心理健康教育']
    if study_type not in valid_type:
        logger.critical('study_type参数错误! 请检查后重新输入!')
        return
    must = [class_info[k]['name']
            for k in class_info.keys() if class_info[k]['type'] == '必修']
    elective = [class_info[k]['name']
                for k in class_info.keys() if class_info[k]['type'] == '选修']
    column = [class_info[k]['name']
              for k in class_info.keys() if class_info[k]['type'] == '专题']
    # 去空格
    must = [i.strip() for i in must]
    elective = [i.strip() for i in elective]
    column = [i.strip() for i in column]
    # 处理不同的身份用户的个性化专栏

    def go_special_page(study_type: str) -> None:
        click_page.ele(f'tag:a@@text():{study_type}').click()
        time.sleep(1)
        kcs = click_page.eles('.kclist')
        for kc in kcs:
            kc_name = kc.ele('.kcmc').text.strip()
            if kc_name in column:
                continue
            else:
                kc.ele('.xx').click()
                time.sleep(1)
                click_page.wait.new_tab(timeout=3)
                tab = click_page.latest_tab
                try:
                    tab.ele('tag:input@@text():继续学习').click()
                except BaseException:
                    pass
                time.sleep(5)
                click_page.close_tabs([tab])
                time.sleep(5)
        pass
    # 所有用户都需要进入的视频

    def go_video_page(course_type: str) -> None:
        if len(must) >= 10 and len(elective) >= 10 and len(column) >= 10:
            return
        if course_type == '专题':
            course_type = '专栏学习'
        dic = {'必修': must, '选修': elective, '专栏学习': column}
        # 进入视频一次页
        click_page.ele(f'tag:a@@text():{course_type}').click()
        time.sleep(1)
        kcs = click_page.eles('.kclist')
        for kc in kcs:
            kc_name = kc.ele('.kcmc').text.strip()  # 空格太抽象了 :)
            if kc_name in dic[course_type]:
                continue
            else:
                kc.ele('.xx').click()
                click_page.wait.new_tab(timeout=3)
                time.sleep(1)
                tab = click_page.latest_tab
                try:
                    tab.ele('tag:a@@text():继续学习').click()
                except BaseException:
                    pass
                time.sleep(5)
                click_page.close_tabs([tab])
                time.sleep(5)
    if len(must) < 10:
        go_video_page('必修')
    if len(elective) < 10:
        go_video_page('选修')
    if len(column) < 10:
        go_video_page('专题')
    go_special_page(study_type)
# 读取课程数量信息


def init(study_type: str = '网络文明志愿者'):
    '''
    初始化，检测是否需要进入视频一次页以及进行进入视频一次操作
    '''
    # 获取课程数量信息
    get_info()
    class_info = json.load(open('course_info.json', 'r'))
    # 读取各个类别的课程数量
    cnt = Counter(class_info[k]['type'] for k in class_info.keys())
    # 检测是否存在小于10的课程数量
    less_10 = [k for k, v in cnt.items() if v < 10]
    if not less_10:
        # 直接进行刷课和检测
        logger.info('所有课程数量均大于10,无需初始化')
        return
    else:
        logger.debug(f'存在课程数量小于10的课程类型:{less_10}')
        logger.debug('正在进行初始化...')
        '''
        回到首页,逐个点击相应视频,每个视频页面停留3秒后推出,并进入下一个视频。
        结束调用get_info()函数，更新课程数量信息
        '''
        # 接管当前页面
        page = ChromiumPage()
        # 进入青马课堂页
        login(first=True, init=True)
        page.ele('tag:a@@text():青马课堂').hover()
        page.ele('tag:a@@text():全部').click()
    click_videoes(study_type=study_type, class_info=class_info)


if __name__ == '__main__':
    init()
