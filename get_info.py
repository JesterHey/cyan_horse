from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import *
from collections import *
import time
import json
from loguru import logger
import subprocess
from typing import *
from get_in import create_login_window
# http://hnqmgc.17el.cn/grzx/

# 单独实现登录操作


def get_into_center(cpage: ChromiumPage):
    cpage.ele('#login_btn').click()
    cpage.ele('@value=进入个人中心').click()


def login(first: bool = True, init: bool = False, username: str = None, pwd: str = None):
    if not first:
        return
    # 先检查当前页面是否已经登录
    page = ChromiumPage()
    try:
        if page.ele('tag:div@@text():欢迎您，', timeout=3):
            logger.info('当前页面已登录')
            return
    except BaseException:
        logger.info('准备登录')
    if first:
        try:
            page.get('http://hnqmgc.17el.cn/grzx/',
                     retry=5, timeout=5, interval=1)
        except BaseException:
            logger.error('网络连接失败')

        # 定位到账号文本框，获取文本框元素
        ele = page.ele('#userName')  # 的意思是通过id定位元素
        try:
            # 输入对文本框输入账号
            ele.input(username)
            # 定位到密码文本框并输入密码
            page.ele('#password').input(pwd)
            # 定位到验证码文本框并输入验证码
            inpcode = page.ele('#yzcode').text  # 湖南青马太可爱了吧，验证码居然直接放在页面源码里:)
            page.ele('#inpcode').input(inpcode)
            # 点击登录按钮
            page.ele('#btnLogin').click()
            page.wait.new_tab(3)
            if page.ele('@onclick=cha()',timeout=3):
                pass
        except BaseException:
            logger.error('登录错误，请检查输入的账号密码是否正确！')
        # 进入课程页面
        try:
            if page.ele('@onclick=cha()', timeout=3):
                page.ele('@onclick=cha()').click()
            # <img style="width: 25px;height: 25px;" src="/images/index/cha.png" alt="" srcset="">
            elif page.ele('tag:img@@style=width: 25px;height: 25px;', timeout=3):
                page.ele('tag:img@@style=width: 25px;height: 25px;').click()
        except BaseException:
            logger.error('不能进入课程页面')
            subprocess.run(["python", __file__])
            exit()
        if not init:
            get_into_center(page)


def get_info(first: bool = True):
    # 创建页面对象，并启动或接管浏览器
    page = ChromiumPage()
    try:
        info = json.load(open('info.json', 'r'))
    except BaseException:
        create_login_window()
        info = json.load(open('info.json', 'r'))
    username = info['username']
    pwd = info['password']
    # 登录
    login(first, init=False, username=username, pwd=pwd)
    # 提取课程信息
    time.sleep(2)
    if not first:
        page.refresh()
        time.sleep(2)
    page.ele('@value=0', timeout=3).click()
    # 获取总页数
    course_info = {}
    logger.debug('读取课程信息中...')
    while 1:
        # 逐页读取课程信息和完成状态并存放到字典中
        tbodys = page.ele('#tbody')
        # 获取tbody下的所有tr
        trs = tbodys.eles('tag:tr')
        for tr in trs:
            cur_info = tr.text.split('\t')
            course_id = cur_info[0]  # 课程id
            course_name = cur_info[1]  # 课程名称
            course_type = cur_info[2]  # 课程类型
            course_rate = int(cur_info[3][:-1])  # 课程完成百分比
            course_status = cur_info[4]  # 课程完成状态(是否完成习题/评价)
            # 存放到字典中
            course_info[course_id] = {
                'name': course_name, 'type': course_type, 'rate': course_rate, 'status': course_status}
        try:
            page.ele('@title=Next page').click()
            time.sleep(1)
        except BaseException:
            break
    logger.success('课程信息读取完成,共有{}门课程'.format(len(course_info)))
    # 写入json文件中
    with open('course_info.json', 'w') as f:
        json.dump(course_info, f)


if __name__ == '__main__':
    create_login_window()
    get_info()
