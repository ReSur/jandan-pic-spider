__author__ = 'ReSur'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding( 'utf-8' )

class website(object):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    def __init__(self, url, ext):
        self.url = url
        self.exurl = url + ext
    def getPage(self, patt):
        print '获取中...'
        pattern = re.compile(patt, re.S)
        try:
            request = urllib2.Request(self.url, headers = self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            item = re.search(pattern, content)
            if item:
                return item.group(1)
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'reason'):
                print e.reason
    def getPages(self, patt, file_name_ext, start, end):
        pattern = re.compile(patt, re.S)
        if start == end - 1:
            file_name = 'results_' + file_name_ext + str(start) + '.txt'
        else:
            file_name = 'results_' + file_name_ext + str(start) + '-' + str(end - 1) + '.txt'
        for page in range(start, end):
            print '正在分析第', str(page), '页'
            current_url = self.exurl + str(page)
            try:
                request = urllib2.Request(current_url, headers = self.headers)
                response = urllib2.urlopen(request)
                content = response.read().decode('utf-8')
                items = re.findall(pattern, content)
                contents = ''
                for item in items:
                    for element in item:
                        contents = contents + element + '\n'
            except urllib2.URLError, e:
                if hasattr(e, 'code'):
                    print e.code
                if hasattr(e, 'reason'):
                    print e.reason
            file = open(file_name, 'a')
            file.write(contents)
            print '已写入第', str(page), '页'
        print '操作结束！'

start_page = 4000
jandan = website('http://jandan.net/pic/', 'page-')
print '自动获取最新页码'
latest_page = int(jandan.getPage('<span class="current-comment-page">\[(.*?)\]</span>'))
print '最新页为：' + str(latest_page)
def valCheck(msg, default):
    trigger = True
    while trigger:
        try:
            trigger = False
            temp = raw_input(msg)
            if temp == '':
                return default
            input_val = int(temp)
        except ValueError:
            trigger = True
    return input_val
def pageCheck(page):
    if page > latest_page:
        print '现在还没有到' + str(page) + '页哦，已替换成最大值［' + str(latest_page) + '］'
        return latest_page
    if page < start_page:
        print '煎蛋关闭了小于' + str(start_page) + '页的旧存档，已替换成最小值［' + str(start_page) + '］'
        return start_page
    return page
last_page = valCheck('请输入［结束页码］，回车自动选择最新页：', latest_page)
last_page = pageCheck(last_page)
first_page = valCheck('请输入［起始页码］，回车自动选择同一页：', last_page)
first_page = pageCheck(first_page)
if cmp(first_page, last_page) == 1:
    first_page, last_page = last_page, first_page
def select_result():
    global patt
    global file_name_ext
    rich_result = raw_input('获取PO主及OOXX数吗？Y/N：')
    if rich_result in ('y', 'Y'):
        patt = '<div class="author.*?<strong.*?">(.*?)</strong>.*?<span class="righttext.*?<a href="(.*?)">(.*?)</a>.*?<p>(.*?)</p>.*?<span id="cos_support-.*?">(.*?)</span>.*?<span id="cos_unsupport-.*?">(.*?)</span>'
        file_name_ext = 'ooxx_'
        return
    elif rich_result in ('n', 'N'):
        patt = '<span class="righttext.*?<a href="(.*?)">.*?<p>(.*?)</p>'
        file_name_ext = ''
        return
    else:
        select_result()
select_result()
jandan.getPages(patt, file_name_ext, first_page, last_page + 1)