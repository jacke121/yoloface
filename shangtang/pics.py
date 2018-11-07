# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


def get_db(server_ip,url,params=''):
    url = "http://" + server_ip + ":9001/" + url+params
    body = {"dbName": "admin"}
    headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    response = requests.get(url, json=body, headers=headers)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)
    res = json.loads(response.text)
    # 返回信息
    print(res)
    return res
def upload_pic(server_ip,url, dbName,name,paths):
    url="http://"+server_ip+":9001/"+url
    body = {"dbName":dbName,"getFeatrue":0,"qualityThreshold":0.9}
    imgs = list()
    for path in paths:
        with open(path, 'rb') as f:
            imgs.append(('imageDatas', (name, f.read())))

    response = requests.post(url, body,files=imgs)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)
    res=json.loads(response.text)
    # 返回信息
    return res
    # print(response.status_code)
if __name__ == '__main__':
    server_ip = "192.168.55.120"

    # get_db(server_ip,url="verify/target/gets")

    name="lbg"
    paths = ["d:/lbg.jpg", "d:/lbg2.jpg"]
    # paths = ["d:/jiang.png"]
    res=upload_pic(server_ip,url="verify/face/synAdd",dbName="sbd_test01",name=name,paths=paths)
    if res['result'] == "error":
        if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
            print(1)
        print("error", res['errorMessage'])
    elif res['result'] == 'success':
        for person in res['success']:
            print(person['personId'],person['qualityScore'],person['name'])
    #
    # res = create_db(server_ip, url="verify/target/deletes", params="?dbName=aaa4")
    # if res['result'] == "error":
    #     if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
    #         print(1)
    #     print("error", res['errorMessage'])
    # elif res['result'] == 'success':
    #     print("ok", res['data'])