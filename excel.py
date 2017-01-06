#encoding:utf-8
import sys
import os
import datetime
import color
#读取excel数据  sudo easy_install xlrd   sudo python setup.py install
#add by yefei


reload(sys)
sys.setdefaultencoding( "utf-8" )
###########################################################
try:
    import xlrd
    print "xrld模块已安装"
except ImportError:
    print "xrld模块未安装,请输入root密码"
    os.system('sudo easy_install xlrd')
try:
    from xlutils.copy import copy
    print "xlutils模块已安装"
except ImportError:
    print "xlutils模块未安装,请输入root密码"
    os.system('sudo easy_install xlutils')
########################################################################################    
class Interface:
    def __init__(self):
        if not os.path.exists('./Template'):
            os.mkdir('./Template')

########################################################################################
    def writeCookie(self, jsessionid):#写sessionid到cookie.txt
        try:
            file_object = open('cookie.txt', 'w')
            file_object.write(jsessionid)
            file_object.close()
        except Exception,e:
            print "写入 cookie.txt 失败 : " + str(e)
            os._exit(0)

#######################################################################################
    def makeDir(self, dubbo):#创建对应.java的文件夹
        self.Package = dubbo.split('.')[-1]
        APIdir = "./Template/" + self.Package
        if not os.path.exists(APIdir):
            os.mkdir(APIdir)

#######################################################################################
    def writeExcel(self, row, col, value):#写入单元格
        table = self.wb.get_sheet(0)
        table.write(row, col, value)
        self.wb.save('excel.xls')
       
########################################################################################
    def run(self):
        ########################################################################################
        login_page = "http://00.0.00.00:8081/login"#尝试登录api获取jessionid，失败退出
        try:
            import urllib2
            import urllib
            import cookielib
            import re
            #获得一个cookieJar实例
            cookie = cookielib.CookieJar()#cookielib.CookieJar('cookie.txt')
            #cookieJar作为参数，获得一个opener的实例
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。此处伪装的火狐
            opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36')]
            #生成Post数据，含有登陆用户名密码。
            data = urllib.urlencode ({  'account':'',
                                        'password':'',
                                        'verifyCode':'abcd' })
            #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
            op = opener.open(login_page,data)
            data = op.read()
            #cookie.save(ignore_discard=True, ignore_expires=True)
            regex = re.compile(r'Cookie JSESSIONID=(.+) for')
            jsessionid = regex.search(str(cookie))
            if '"code":200' in data:
                print "http://00.0.00.00/api/ 登录成功"
                self.writeCookie(jsessionid.group(1))
            else:
                print "http://00.0.00.00/api/ 用户密码错误"
                os._exit(0)
        except Exception,e:
            print "http://00.0.00.00/api/ 登录失败 : " + str(e) 
            os._exit(0)
        ################################################################################
         # 打开xls文件
        rb = xlrd.open_workbook('excel.xls')
        self.wb = copy(rb)
        table = rb.sheets()[0] # 打开第一张表
        ########################################################################################
        

        
        ########################################################################################
        nrows = table.nrows # 获取表的行数
        #    print "API  number: "  + str(nrows-1)
        for i in range(nrows): # 循环逐行
            title = table.row_values(0)
            line = table.row_values(i)
            if i == 0: # 跳过第一行
                continue
        ########################################################################################
            self.makeDir(line[title.index('dubbo')])#生成对应文件夹

            API = line[title.index('API')]#API
            API.lstrip()

            user = API.split('.')#分割

            description = '"' + line[title.index('description')].lstrip() + '"'
            method = line[title.index('method')].lstrip()
            #user = user[2]
        ########################################################################################
            try:
                if (line[title.index('isLogin')] == 1 and user.count('p')-user.count('d')):#
                    if (user.count('p')):#
                        os.system("python passislogin.py " + API + " " + method + " " + description + " " + self.Package)
                    elif (user.count('d')):#
                        os.system("python drivislogin.py " + API + " " + method + " " + description + " " + self.Package)
                    else:
                        sys.stdout.write(color.UseStyle(API + ' failed1: ', mode = 'bold', fore = 'blue'))
                        print "!"
                elif (line[title.index('isLogin')] > 1):#2
                    if (line[title.index('isLogin')] == 2):#
                        os.system("python passislogin.py " + API + " " + method + " " + description + " " + self.Package)
                    elif (line[title.index('isLogin')] == 3):#
                        os.system("python drivislogin.py " + API + " " + method + " " + description + " " + self.Package)
                    else:
                        sys.stdout.write(color.UseStyle(API + ' failed2: ', mode = 'bold', fore = 'blue'))
                        print "!"
                elif (line[title.index('isLogin')] == 0):#
                    os.system("python nouserlogin.py " + API + " " + method + " " + description + " " + self.Package)
                else :
                    sys.stdout.write(color.UseStyle(API + ' failed3: ', mode = 'bold', fore = 'blue'))
                    print "!"
            except Exception, e:
                sys.stdout.write(color.UseStyle(API + ' failed4: ', mode = 'bold', fore = 'blue'))
                print str(e)
               
########################################################################################
if __name__ == "__main__":
    starttime = datetime.datetime.now()
    iGet = Interface()
    iGet.run()
    endtime = datetime.datetime.now()
    sys.stdout.write(color.UseStyle('用时:', mode = 'bold', fore = 'blue'))
    print color.UseStyle(' %f s' % ((endtime - starttime).seconds), fore = 'red')
    

