# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
def upload_pic(server_ip,url, param="aaa4"):
    url="http://"+server_ip+":9001/"+url#+param
    print(url)
    body = {"dbName":"aaa4"}
    paths=["d:/f1.jpg","d:/f2.jpg"]
    imgs=list()
    for path in paths:
        with open(path, 'rb') as f:
            imgs.append(('imageDatas', (path, f.read())))
    response = requests.post(url, body,files=imgs)
    res=json.loads(response.text)
    # 返回信息
    print(res)
    return res

if __name__ == '__main__':
    server_ip = "192.168.55.120"
    res=upload_pic(server_ip,url="verify/face/synAdd",param="?dbName=aaa4&imageDatas=1354")
    if res['result'] == "error":
        if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
            print(1)
        print("error", res['errorMessage'])
    elif res['result'] == 'success':
        print("ok", res['success'])