from DrissionPage import ChromiumPage
from DrissionPage.common import *
from collections import *
import json
from single_course import one_course
from loguru import logger


def kill_course(again: bool = False):
    # 统计课程完成情况
    cnt = defaultdict(list)
    # 读取课程信息
    info = json.load(open('course_info.json', 'r'))
    # 统计各个类别的课程 = 100的数量
    cnt2 = Counter(info[k]['type']
                   for k in info.keys() if info[k]['rate'] == 100)
    for k, v in info.items():
        if v['rate'] < 100 and cnt2[v['type']] < 10:
            cnt[v['type']].append((k, v['rate']))  # 课程类型作为键，课程id作为值
    logger.info('{}'.format(cnt))
    if not cnt:
        logger.info('所有课程均已完成')
        return
    # 按必修-选秀-专题-培训执行刷课
    must = cnt['必修']
    elective = cnt['选修']
    special = cnt['专题']
    train = cnt['培训']
    while must or elective or special or train:
        if must:
            course_info = must.pop()
            logger.info('当前刷课序号:{}'.format(course_info[0]))
            one_course(course_info[0], '必修', course_info[1], again=again)
        if elective:
            course_info = elective.pop()
            logger.info('当前刷课序号:{}'.format(course_info[0]))
            one_course(course_info[0], '选修', course_info[1], again=again)
        if special:
            course_info = special.pop()
            logger.info('当前刷课序号:{}'.format(course_info[0]))
            one_course(course_info[0], '专题', course_info[1], again=again)
        if train:
            course_info = train.pop()
            logger.info('当前刷课序号:{}'.format(course_info[0]))
            one_course(course_info[0], '培训', course_info[1], again=again)


if __name__ == '__main__':
    kill_course()
