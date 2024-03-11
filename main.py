import json
from get_info import get_info
from collections import *
from loguru import logger
import subprocess
from typing import *
from DrissionPage import ChromiumPage
from DrissionPage.common import *
import time
# 获取课程信息
get_info()
# 执行刷课
from kill_course import kill_course
kill_course()
# 完成刷课后，判定是否存在需要答题或者评分的课程
'''
重新检测各个课程的status参数
1. 对于必修课存在3种情况:未完成，已完成，未答题
2. 对于其他课存在3种情况:未完成，已完成，未评分
'''
# 重新获取课程信息
def new_info() -> DefaultDict[str, List[Tuple[str,int,str]]]:
    get_info(first=False)
    new_info = json.load(open('course_info.json','r'))
    # 读取各个类别的课程状态
    new_cnt = defaultdict(list)
    for k, v in new_info.items():
        new_cnt[v['type']].append((k,v['rate'],v['status'])) # 课程类型作为键，课程id作为值
    return new_cnt

new_cnt = new_info()
# 首先检查是否还存在未完成的课程
for k, v in new_cnt.items():
    for i in v:
        if i[1] < 100:
            logger.error('存在未完成的课程:{}! 将重新执行刷课'.format(i[0]))
            # 完全关闭进程并重新执行刷课
            kill_course(again=True)
            subprocess.run(["python", __file__])
            exit()

# 若上述检验通过，则重新读取课程信息并检验是否存在未答题或者未评分的课程
new_cnt = new_info()
not_judged = []
not_quiz = []
for k, v in new_cnt.items():
    for i in v:
        if i[2] == '未评分':
            not_judged.append((i[0],k))
        elif i[2] == '未答题':
            not_quiz.append(i[0],k)


# 实现自动评分
def auto_judge(course_id:str,course_type:str) -> None:
    # 根据课程类型和id进行定位
    j_page = ChromiumPage() # 接管当前页面
    # 判定课程类别
    if course_type == '必修':
        j_page.ele('@value=1').click()
    elif course_type == '选修':
        j_page.ele('@value=2').click()
    elif course_type == '专题':
        j_page.ele('@value=4').click()
    elif course_type == '培训':
        j_page.ele('@value=5').click()
    time.sleep(1)
    trs = j_page.ele('#tbody').eles('tag:tr')
    for tr in trs:
        # 鉴别课程序号
        if tr.ele('tag:td').text.split('\t')[0] == course_id:
            # 进入评分页面
            tr.ele('tag:button@@text():进入评分').click()
            j_page.ele('x://*[@id="gradeDetail_score"]/label[1]/input').click()
            j_page.ele('tag:a@@text():保存').click()
            time.sleep(1)
    pass
# 实现自动评分
if not_judged:
    for i in not_judged:
        logger.info('正在对课程:{}进行评分'.format(i[0]))
        auto_judge(i[0],i[1])
        logger.success('已完成对课程:{}的评分'.format(i[0]))
else:
    logger.info('没有需要评分的课程')
# 实现题目答案显示
def auto_quiz(course_id:str) -> None:
    pass
if not_quiz:
    for i in not_quiz:
        logger.info('正在获取课程:{}的答案'.format(i[0]))
        auto_quiz(i[0])
        logger.success('已完成对课程:{}的答案获取'.format(i[0]))
else:
    logger.info('没有需要答题的课程')

# 重新检验是否存在未评分或者未答题的课程
logger.debug('正在进行最终检验...')
time.sleep(2)
new_cnt = new_info()
not_judged = []
not_quiz = []
for k, v in new_cnt.items():
    for i in v:
        if i[2] == '未评分':
            not_judged.append((i[0],k))
        elif i[2] == '未答题':
            not_quiz.append(i[0],k)
if not not_judged and not not_quiz:
    logger.warning('所有课程均已完成,页面即将关闭')
    page = ChromiumPage()
    page.close_tabs()
else:
    subprocess.run(["python", __file__])
    exit()