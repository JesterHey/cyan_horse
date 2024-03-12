from DrissionPage import ChromiumPage
from DrissionPage.common import *
from loguru import logger
import subprocess
from get_info import login
# page = ChromiumPage()
# page.get('http://hnqmgc.17el.cn/')
# try:
#     if page.ele('@onclick=cha()',timeout=3):
#         page.ele('@onclick=cha()').click()
#     # <img style="width: 25px;height: 25px;" src="/images/index/cha.png" alt="" srcset="">
#     elif page.ele('tag:img@@style=width: 25px;height: 25px;',timeout=3):
#         page.ele('tag:img@@style=width: 25px;height: 25px;').click()
# except BaseException:
#     logger.error('不能进入课程页面')
#     subprocess.run(["python", __file__])
#     exit()
# page.ele('tag:a@@text():青马课堂').hover()
# page.ele('tag:a@@text():全部').click().for_new_tab()
login(first=True,init=True)