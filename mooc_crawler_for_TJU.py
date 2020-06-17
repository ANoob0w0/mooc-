#coding=utf-8
import requests
import time
import re
from bs4 import BeautifulSoup
from PIL import Image

#超星模拟登录
header = {
        'Referer': 'http://tju.boya.chaoxing.com/portal',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}
name = input("输入学号:")
password = input("输入密码:")
num = int(time.time()) #时间戳，取整
code_url = 'http://passport2.chaoxing.com/num/code/?'+str(num) #图片url
session = requests.Session()
r=session.get(code_url)
image = r.content
with open('code.jpg','wb') as f:
    f.write(image)
img = Image.open('code.jpg')
img.show()
numcode = input("输入验证码:")
#post的参数
params = {
    'refer_0x001':'http%3A%2F%2Fi.mooc.chaoxing.com',
    'pid':'1',
    'pidName':'',
    'fid':'122191',
    'fidName':'天津大学研究生院',
    'allowJoin':'0',
    'isCheckNumCode':'1',
    'f':'0',
    'uname':name,
    'password':password,
    'numcode':numcode
}
url = 'http://passport2.chaoxing.com/login' #form提交的url
session.post(url,params,headers=header)
print('登录成功！')
get_url_idpage = input("请输入课程列表网址:")
#knowledgeid=session.get(url = get_url_knowledgeid,headers = header) #再次使用session进行请求的发送，该次请求中已经携带了cookie 
#knowledgeid.encoding = 'utf-8'

# type(knowledgeid) 		#查看类型
# print(knowledgeid.text[:1500])	#显示前1500字节内容
# print(knowledgeid.status_code)    #显示状态码

def getHTML(url,header):
    try:
        r = session.get(url,headers = header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

""" def find_href(raw_page):
    links_list = []
    bsObj = BeautifulSoup(raw_page.text, 'html.parser')
    t1 = bsObj.find_all('a')
    for t2 in t1:
        t3 = t2.get('href')
        links_list.append(t3)
    return links_list """

def find_links(tr):
    try:
        tr = (re.findall(r'<a href=(.*?)">',tr,re.S))
        return tr
    except:
        return ""

def get_id_titles(r):
    try:
        r = r[r.find('chapterId=')+10:r.find('chapterId=')+19] + ' ' + r[r.find('title=\"')+7:]
        return r
    except:
        return ""


print('正在获取课程id...')

idpage = getHTML(get_url_idpage,header)

id_list = []

for eachlinks in (find_links(idpage)):
    id_list.append(get_id_titles(eachlinks))

for i in range(3):
    del id_list[0]

def get_content(raw_page):
    tr = re.findall(r'>&nbsp;(.*?)</span></p>',raw_page,re.S)
    para = ''
    for item in tr:
        para = para + '\n' +item
    return para

def save_file(text):
    f=open('couses.txt','w')
    for t in text:
        if len(t) > 0:
            f.writelines(t + "\n")
    f.close()

print('正在生成课程url...')
course_url = ''
url_list = []
for eachids in id_list:
    course_url = 'https://mooc1-1.chaoxing.com/knowledge/cards?clazzid=' + get_url_idpage[84:92] + '&courseid=' + get_url_idpage[61:70] + '&knowledgeid='+ eachids[0:9] + '&num=0&ut=s&cpi=116766354&v=20160407-1'
    url_list.append(course_url)

text = []
for urls in url_list:
    r = getHTML(urls,header)
    text.append(get_content(r))

save_file(text)

print('完成！')