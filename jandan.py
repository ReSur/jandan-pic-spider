__author__ = 'ReSur'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class website(object):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    def __init__(self, url, ext):
        self.url = url
        self.exurl = url + ext
    def getPage(self, patt):
        print u'获取中...'
        pattern = re.compile(patt, re.S)
        try:
            request = urllib2.Request(self.url, headers = self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            item = re.search(pattern, content)
            if item:
                return item.group(1)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
    def getPages(self, patt, start, end):
		pattern = re.compile(patt, re.S)
		for page in range(start, end):
		    print u'正在分析第', str(page), u'页'
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
		        if hasattr(e, "code"):
		            print e.code
		        if hasattr(e, "reason"):
		            print e.reason
		    file = open('result.txt', 'a')
		    file.write(contents)
		    print u'已写入第', str(page), u'页'

jandan = website('http://jandan.net/pic/', 'page-')
last_page = str(raw_input('请输入［结束页码］，回车自动获取最新页：'))
if last_page == '':
    last_page = jandan.getPage('<span class="current-comment-page">\[(.*?)\]</span>')
    print u'结束页为', last_page
first_page = str(raw_input('请输入［起始页码］，回车自动选择同一页：'))
if first_page == '':
	first_page = last_page
	print u'起始页为', first_page
def select_result():
	global patt
	rich_result = raw_input("获取PO主及OOXX数吗？，是输入1，否输入0：")
	if rich_result == '1':
	    patt = '<div class="author.*?<strong.*?">(.*?)</strong>.*?<span class="righttext.*?<a href="(.*?)">(.*?)</a>.*?<p>(.*?)</p>.*?<span id="cos_support-.*?">(.*?)</span>.*?<span id="cos_unsupport-.*?">(.*?)</span>'
	    return
	elif rich_result == '0':
	    patt = '<span class="righttext.*?<a href="(.*?)">.*?<p>(.*?)</p>'
	    return
	else:
		select_result()
select_result()
jandan.getPages(patt, int(first_page), int(last_page) + 1)