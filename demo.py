from collections import *
import json
info = json.load(open('course_info.json','r'))
cnt = Counter(info[k]['type'] for k in info.keys())
print(cnt)
cnt['必修'] = 1
less_10 = [k for k, v in cnt.items() if v < 10]
print(less_10)