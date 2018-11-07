
# !/usr/bin/env python
# -*- coding: utf-8 -*-

#354
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
#http://ip:port/verify/target/deletes

def del_db(server_ip,url, dbName="aaa4"):
    url="http://"+server_ip+":9001/"+url+"?dbName="+dbName
    body = {"dbName":"aaa4"}
    headers = {'Content-type': "application/json", 'Accept': 'application/json',}
    response = requests.post(url, data=json.dumps(body))
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)
    res=json.loads(response.text)
    # if res['result'] == "error":
    #     if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
    #         print(1)
    #     print("error", res['errorMessage'])
    # elif res['result'] == 'success':
    #     print("ok", res['data'])
    print(res)
    # 返回信息

    return res

def create_db(server_ip,url, param="aaa4"):
    url="http://"+server_ip+":9001/"+url+param
    body = {"dbName":"aaa4"}
    headers = {'Content-type': "application/json", 'Accept': 'application/json',}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)
    res=json.loads(response.text)
    # 返回信息

    return res
    # print(response.status_code)
#{'dbName': 'aaa4', 'dbId': 'aaa4'}
if __name__ == '__main__':
    server_ip = "192.168.55.120"

    # res= del_db(server_ip, url="verify/target/deletes",dbName="aaa")

    res=create_db(server_ip,url="verify/target/add",param="?dbName=sbd_test01")
    # if res['result'] == "error":
    #     if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
    #         print(1)
    #     print("error", res['errorMessage'])
    # elif res['result'] == 'success':
    #     print("ok", res['data'])
    #
    get_db(server_ip, url="verify/target/gets")
