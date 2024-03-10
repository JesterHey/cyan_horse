import json
from get_info import get_info
from collections import *
from loguru import logger
import subprocess
from typing import *
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
    get_info()
    new_info = json.load(open('info.json','r'))
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
            logger.critical('存在未完成的课程:{}! 将重新执行刷课'.format(i[0]))
            # 完全关闭进程并重新执行刷课
            kill_course(again=True)
            subprocess.run(["python", __file__])
            exit()

# 若上述检验通过，则重新读取课程信息并检验是否存在未答题或者未评分的课程
new_cnt = new_info()
not_judged = []
not_quiz = []
for k, v in new_cnt.items():
    if v['status'] == '已完成':
        continue
    if v['status'] == '未评分':
        not_judged.append(k)
    else:
        not_quiz.append(k)

# 展示提示信息
for i in not_judged:
    logger.warning('存在未评分的课程:{}'.format(i))
# 实现自动评分
def auto_judge(course_id:str) -> None:
    pass
for i in not_judged:
    logger.warning('存在未答题的课程:{}'.format(i))
# 实现自动答题
pass