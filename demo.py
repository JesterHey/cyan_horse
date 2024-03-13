import json
dic = json.load(open('course_info.json', 'r'))
l1 = [ i for i in dic.keys() if dic[i]['type'] == '选修' ]
l2 = [ i for i in dic.keys() if dic[i]['type'] == '必修' ]
l3 = [ i for i in dic.keys() if dic[i]['type'] == '专题' ]
l4 = [ i for i in dic.keys() if dic[i]['type'] == '培训' ]
print(len(l1))
print(len(l2))
print(len(l3))
print(len(l4))