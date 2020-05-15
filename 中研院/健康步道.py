import requests
# from pyquery import PyQuery as pq
#
# # getting data
# res = requests.get("https://www.hpa.gov.tw/Pages/List.aspx?nodeid=332")
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(res.text, 'html.parser')
# # print(soup)
# div_tags = soup.find_all('div', {'class': "col-xs-12 col-sm-10 col-md-10 six-title"}) #找到網頁中全部的 <div class="title">
# print(div_tags)
# # for div_tag in div_tags:
# #     a_tag = div_tag.find('a') #找到 <div class="title"> 下的 <a>
# #     print(a_tag)
# #     if a_tag is not None: #或文章被刪除會是None，所以要排除None
# #         print(a_tag.text)
#引入系统类库
import sys
# 使用文档解析类库
from bs4 import BeautifulSoup
# 使用网络请求类库
import urllib.request
# 输入网址
import requests
from pyquery import PyQuery as pq

# res = requests.get("https://www.hpa.gov.tw/Pages/List.aspx?nodeid=332")
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(res.text, 'html.parser')
# # print(soup)
html_doc = "https://www.hpa.gov.tw/Pages/List.aspx?nodeid=332"
if len(sys.argv) > 1:
   website = sys.argv[1]
   if(website is not None):
        html_doc = sys.argv[1]
# 获取请求
req = urllib.request.Request(html_doc)
# 打开页面
webpage = urllib.request.urlopen(req)
# 读取页面内容
html = webpage.read()
# 解析成文档对象
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# # 非法URL 1
invalidLink1 = '#'
# 非法URL 2
invalidLink2 = 'javascript:void(0)'
# 集合
result = set()
# 计数器
mycount = 0
# 查找文档中所有a标签
for k in soup.find_all('a'):
    print(k)
    # 查找href标签
    link = k.get('href')
    # 过滤没找到的
    if(link is not None):
          #过滤非法链接
          if link==invalidLink1:
            pass
          elif link==invalidLink2:
            pass
          elif link.find("javascript:")!=-1:
            pass
          else:
            mycount=mycount+1
            #print(mycount,link)
            result.add(link)
print("打印超链接个数:",mycount)
print("打印超链接列表",result)
