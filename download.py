#!/usr/bin/python3
#-*-coding:utf-8-*- 
import requests
import os

# url = 'http://artimages.clevelandart.org/zoomify/484A45A05B4D576545F511FE922B9486/TileGroup0/{0}'
url = 'http://artimages.clevelandart.org/zoomify/{0}/TileGroup{1}/{2}'
errorNum = 0
tileGroup = 0
zoomcode = ''
x = 5
y = 0
z = 0
filename = '{0}-{1}-{2}.{3}'
postfix = ''
dir_path = ''
proxies = {}
callback = None
# proxies = {
#     "http": "socks5://127.0.0.1:1080", 
#     "https": "socks5://127.0.0.1:1080"
#     }


def init(code, start_img, start_path, http_proxy, https_proxy, outputInfo):
    global url
    global x
    global y
    global z
    global dir_path
    global postfix
    global zoomcode
    global proxies
    global callback
    callback = outputInfo
    if http_proxy:
        proxies['http'] = http_proxy
    if https_proxy:
        proxies['https'] = https_proxy
        callback(1, '代理地址：'+str(proxies))
    try:
        start_img_name = start_img.split('.', 1)[0]
        postfix = start_img.split('.', 1)[1]
        x = int(start_img_name.split('-')[0])
        y = int(start_img_name.split('-')[1])
        z = int(start_img_name.split('-')[2])
    except Exception as err:
        callback(2, err.message)
        callback(0)
    zoomcode = code 
    dir_path = start_path
    if not os.path.exists(start_path):
        os.mkdir(start_path)


def download():
    global errorNum
    global x
    global y
    global z
    global postfix
    global tileGroup
    nf = filename.format(x, y, z, postfix)
    newurl = url.format(zoomcode, tileGroup, nf)
    response = requests.get(newurl, proxies=proxies)
    if response.status_code == 404:
        callback(2, nf+' Not found')
        errorNum += 1
        if errorNum == 1:
            tileGroup += 1
            download()
        elif errorNum == 2:
            tileGroup = 0
            z = 0
            y += 1
            download()
        else:
            callback(1, '下载完成')  # 输出信息
            return
    else:
        img = response.content
        errorNum = 0
        z += 1
        with open(dir_path+'/'+nf, 'wb') as f:
            f.write(img)
        callback(1, nf+' 下载完成')
        download()


# if __name__ == '__main__': 
#     download()