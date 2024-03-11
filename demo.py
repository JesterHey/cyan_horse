from collections import *
import json
info = json.load(open('course_info.json', 'r'))
cnt = defaultdict(list)
new_cnt = defaultdict(list)
for k, v in info.items():
    new_cnt[v['type']].append((k,v['rate'],v['status'])) # 课程类型作为键，课程id作为值
print(new_cnt)
for k,v in new_cnt.items():
    print(k,v)