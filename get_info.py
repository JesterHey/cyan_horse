from DrissionPage import WebPage
from DrissionPage.common import *
from collections import *
import time
import json
from loguru import logger
# http://hnqmgc.17el.cn/grzx/

def get_info():
    # 创建页面对象，并启动或接管浏览器
    page = WebPage()
    # 跳转到登录页面
    try:
        page.get('http://hnqmgc.17el.cn/grzx/',retry=5,timeout=5,interval=1)
    except BaseException:
        logger.error('网络连接失败')

    # 定位到账号文本框，获取文本框元素
    ele = page.ele('#userName') # #的意思是通过id定位元素
    # 输入对文本框输入账号
    ele.input('51140220050507901X')
    # 定位到密码文本框并输入密码
    page.ele('#password').input('hnqm123456')
    # 定位到验证码文本框并输入验证码
    inpcode = page.ele('#yzcode').text # 湖南青马太可爱了吧，验证码居然直接放在页面源码里:)
    page.ele('#inpcode').input(inpcode)
    # 点击登录按钮
    page.ele('#btnLogin').click()
    # 进入课程页面
    page.ele('.wxtsBox-button').click() # 关闭提示页面
    page.ele('#login_btn').click()
    page.ele('@value=进入个人中心').click()
    # 提取课程信息
    time.sleep(2)
    page.ele('@value=0').click()
    # 获取总页数
    course_info = {}
    # <div class="paginationjs-nav J-paginationjs-nav">1 / 4</div>
    # total_page = int(page.ele('.paginationjs-nav J-paginationjs-nav').text)
    total_page = 4
    for i in range(total_page):
        # 逐页读取课程信息和完成状态并存放到字典中
        tbodys = page.ele('#tbody')
        # 获取tbody下的所有tr
        trs = tbodys.eles('tag:tr')
        for tr in trs:
            cur_info = tr.text.split('\t')
            course_id = cur_info[0]  # 课程id
            course_type = cur_info[2] # 课程类型
            course_rate = int(cur_info[3][:-1])  # 课程完成百分比
            course_status = cur_info[4]  # 课程完成状态(是否完成习题/评价)
            logger.info('课程id:{}|课程类型:{}|课程完成率:{}|课程完成状态:{}'.format(course_id,course_type,course_rate,course_status))
            # 存放到字典中
            course_info[course_id] = {'rate': course_rate,'type': course_type,'status': course_status}
        if i != total_page - 1:
            page.ele('@title=Next page').click()
            time.sleep(1)
    print(len(course_info))
    # 写入json文件中
    with open('course_info.json', 'w') as f:
        json.dump(course_info, f)

if __name__ == '__main__':
    get_info()