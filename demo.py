from DrissionPage import ChromiumPage
from DrissionPage.common import *
page = ChromiumPage()
page.ele('tag:a@@text():是').click()