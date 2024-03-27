# coding=utf-8
import os
from bs4 import BeautifulSoup
import sys

#定义一个list来存放文件路径
paths=[]

#获取所有的文件路径
def get_paths():
    for fpathe,dirs,fs in os.walk('html'):
        for f in fs:
            #print os.path.join(fpathe,f)
            #将拼接好的path存放到list中
            filepath=os.path.join(fpathe,f)
            #只放入.html后缀文件路径
            if(os.path.splitext(f)[1]==".html"):
                paths.append(filepath)

#读取html文件修改后并写入相应的文件中去
def reset_file(path):
    #判断文件是否存在
    if not os.path.isfile(path):
        raise TypeError(path + " does not exist")

    #读取文件,bs4自动将输入文档转换为Unicode编码，
    #输出文档转换为utf-8编码,bs4也可以直接读取html
    #字符串，例如BeautifulSoup('<div>content</div>')
    soup=BeautifulSoup(open(path))

    #select是bs4提供的方法，和jquery的$选择器一样
    #方便。可以标签(eg:div,title,p...)来查找,也
    #也可以通过css的 class .和id #来查找，基本上和我们
    #使用$一样。

    #选取id="nav"节点下的所有li元素里面的a标签，返回值是一个list集合
    nav_a=soup.select("#nav li a")

    #修改a的href属性
    if(len(nav_a)>1):
        nav_a[0]["href"]="/m/"
        nav_a[1]["href"]="/m/about_mobile/m_about.html"

    #选取class="footer"里的所有a标签
    footer_a=soup.select(".footer a")
    if(len(footer_a)>0):
        footer_a[1]["href"]="/m/about_mobile/m_sjdt.html"

    content_p=soup.select(".content p")
    #修改<p>我是string</p>里面的文本内容
    if(len(content_p)>0):
        content_p[0].string="修改p标签里面的测试内容"

    #修改系统的默认编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #打开相应的文件写入模式，打开文件不要放入try里面，否则会
    #出现异常
    f=open(path,"w")
    try:
        #写入文件
        f.write(soup.prettify())
    finally:
        #关闭文件
        file.close()

#定义main函数程序的入口
if __name__=="__main__":
    get_paths()
    #遍历所有文件路径
    for p in paths:
        reset_file(p)
