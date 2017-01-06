#encoding=utf8
import sys  
import urllib2  
import re 
import color

#查询到对应接口，找到接口的网页
def getAPIURL(html):
    reg = r'href="(/api/test.*)">测试</a>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    for imgurl in imglist:
        return 'http://10.0.53.71:8081' + imgurl

#根据接口抓取入参
def getParameter(html):
    #reg = r'<label for="activityId">.+(.+?)'
    #imgre = re.compile(reg,re.S)
    imglist = re.findall(r'<label for=".+\r\n\s+([a-zA-Z]+)-(.+)\r\n\s+-([非必填]+)',html)
    #print imglist[0][1]
    return imglist

def html(url):
    ###################################################
    file_object = open('cookie.txt')
    try:
        jsessionid = file_object.read()
    finally:
        file_object.close()
    ###################################################
    headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                'Connection':'keep-alive',
                'Cookie':'JSESSIONID=' + jsessionid,
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
              }

    #通过urllib2提供的request方法来向指定Url发送我们构造的数据
    try:
        request = urllib2.Request(url, headers=headers)#访问查询接口网页
        response = urllib2.urlopen(request)
        html = response.read()
        request = urllib2.Request(getAPIURL(html), headers=headers)#访问接口测试网页
        response = urllib2.urlopen(request)
        html = response.read()
        return getParameter(html)#根据html获取入参
    except Exception, e:
        #'http://00.0.00.00:8081/api/index?keywords=' + Apiname + '&product=0&class1=0'
        API = re.findall(r'keywords=(.+)&product=0&class1=0',url)
        sys.stdout.write(color.UseStyle(API[0], mode = 'bold', fore = 'blue'))
        sys.stdout.write(color.UseStyle("  failed: ", fore = 'red'))
        print str(e)
        return False

#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）  
#html(posturl)

#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
