# -*- coding:utf-8 -*-
import re
from requests import request
UA = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"

class SpiderBase(object):
    def __init__(self, user_agent=UA, *args, **kwargs):
        self.user_agent = user_agent
        self.headers = {"User-Agent": self.user_agent}

class QSBK(SpiderBase):
    def __init__(self, url="", **kwargs):
        super(QSBK, self).__init__(**kwargs)
        self.url = url
        self.item_joke = []

#请求
    def get_content(self, page):
        # request = urllib.request.Request(self.url + str(page), headers=self.headers)
        response = request('GET', self.url + str(page), headers=self.headers)
        if response.status_code == 200:
            content = response.text
            return content
        else:
            raise Exception(u"请求失败")

#处理逻辑===正则
    def get_jokeRegular(self, content):
         print("start get_jonkeRegular")
         #.匹配所有 *是0个或者多个 ？是非贪婪模式 \s空格
         pattern = re.compile(
             # '<div.*?class="author.*?.<span><img\s+src="(.*?)".*/>.*?</span>'#头像
             #                  '.*?'
                              '<h2>(.*?)</h2>'#姓名。
                              '.*?'
                              '<div.*?class="articleGender(.*?)Icon">(.*?)</div>'#性别 年龄
                              '.*?'
                              '<div.*?class="content".*?.<span>(.*?)</span>'#内容
                              , re.S)

         #append列表追加
         self.item_joke.extend(re.findall(pattern, content))
         print("end jokeRegular")

    def logic(self):
        page = input('请输入爬取的页面:')
        for i in range(int(page)):
            content = self.get_content(i + 1)
            self.get_jokeRegular(content)
        print('输出段子')
        i = 0
        print('每按一次快捷键(回车)读取一条段子,按Q退出')
        for item in self.item_joke:
            input_content = raw_input()
            if input_content != "Q":
                i += 1
                print(
                    # "头像:" + item[0] + "\n" +
                      u"作者:" + item[0] + "\n" +
                      u"性别:" + item[1] + "\n" +
                      u"年龄:" + item[2] + "\n" +
                      u"内容:" + item[3] + "\n")
                print(u'段子输出完毕!\n段子数量为:%s' % i)
            else:
                print(u"退出")
                return

qsbk = QSBK(url='http://www.qiushibaike.com/hot/page/')
qsbk.logic()

# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent': user_agent}
# try:
#     # request = urllib2.Request(url, headers=headers)
#     # response = urllib2.urlopen(request)
#     # print response.read()
#     request = urllib2.Request(url, headers=headers)
#     response = urllib2.urlopen(request)
#     content = response.read().decode('utf-8')
#     pattern = re.compile(
#         # '<div.*?class="thumb".*?.<a.*?<img.*?src="(.+?\.jpg)".*?alt=".*?"/>.*?</a>'
#         # '.*?'
#         '<h2>(.*?)</h2>'#姓名
#         '.*?'
#         '<div.*?class="content".*?.<span>(.*?)</span>'#内容
#         , re.S)
#     items = re.findall(pattern, content)
#     for item in items:
#         # haveImg = re.search("img", item[0])
#         # print "-------", item[0], "ljhll", haveImg
#         # if not haveImg:
#         #     print item[1], item[2]
#         # else:
#         print item[0], item[1]
# except urllib2.URLError, e:
#     if hasattr(e, "code"):
#         print e.code
#     if hasattr(e, "reason"):
#         print e.reason