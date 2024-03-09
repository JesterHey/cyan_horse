from DrissionPage import ChromiumPage
from DrissionPage.common import *
from collections import *
import time
import json
# 统计课程完成情况
cnt = defaultdict(list)
# 读取课程信息
info = json.load(open('course_info.json', 'r'))
for k, v in info.items():
    if v['rate'] < 100:
        cnt[v['type']].append(k)
print(cnt)
# 按必修-选秀-专题-培训执行刷课
must = cnt['必修']
elective = cnt['选修']
special = cnt['专题']
train = cnt['培训']
while must or elective or special or train:
    if must:
        course_id = must.pop()
        print('Kill course:', course_id)
        # 执行刷课
        # ...
    if elective:
        course_id = elective.pop()
        print('Kill course:', course_id)
        # 执行刷课
        # ...
    if special:
        course_id = special.pop()
        print('Kill course:', course_id)
        # 执行刷课
        # ...
    if train:
        course_id = train.pop()
        print('Kill course:', course_id)
        # 执行刷课
        # ...