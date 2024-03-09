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