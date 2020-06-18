import requests
import json
import re

def get_html():
    res = requests.get('https://api.bilibili.com/x/web-interface/index/icon?spm_id_from=333.788.b_636f6d6d656e74.132')
    data = json.loads(res.content.decode())
    links = 'http:' + data['data']['icon']
    name = data['data']['title'] + ' .gif'
    ids = data['data']['id']
    return links,name,ids

def check_name(name):
    #名字中不能有? * / \ < > : " |
    new_name = re.sub(r'[\?\*\/\\\<\>\:\"\|]','',name)
    return new_name

def main():
    cnt = 0
    id_list = []
    while cnt <= 10:
        data = get_html()
        links = data[0]
        name = data[1]
        ids = data[2]
        if(id_list.count(ids) == 0):
            id_list.append(ids)
            with open(check_name(name),"wb") as f:
                with requests.get(links) as r:
                    f.write(r.content)
        else:
            cnt += 1

main()

print("完成！")