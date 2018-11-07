# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

def creat_task(server_ip,url, dbName,call_ip,video_path):
    url="http://"+server_ip+":80/"+url
    print(url)
    body = {}
    body["taskType"] = 0  # , // 任务类型固定填 0
    body["param"] = {}
    body["param"]["Source"] = {}
    body["param"]["Source"]["SourceType"] = 0
    body["param"]["Source"]["VideoFile"] = video_path
    body["param"]["Source"]["Looplay"] = 0
    body["Result"] = []
    body["Result"].append({"Index": 0, "ProtocolType": 10, "URL": call_ip})
    body["Result"].append({"Index": 1, "ProtocolType": 10, "URL": call_ip})
    body["Private"]={}
    body["Private"]["targets"]=[]
    body["Private"]["targets"].append({"dbId": dbName, "score": 0.3})

    response = requests.post(url, json.dumps(body))
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    if response.status_code==404:
        print("error 404")
        return response.text
    res=json.loads(response.text)
    # 返回信息
    return res

def create():
    server_ip = "192.168.55.120"

    call_ip = "192.168.25.68:9999"
    # get_db(server_ip,url="verify/target/gets")

    # path="rtsp://admin:sbdwl123@192.168.25.41:554/h264/ch1/main/av_stream"
    path = "d:/2.mp4"
    res = creat_task(server_ip, url="Task/CreateTask?ProjectID=1000", dbName="aaa3", call_ip=call_ip, video_path=path)
    print(res)
    if '<html>' in res:
        print("error")
    elif res['returnCode'] == 0:
        print(res['taskID'])

    elif res['returnCode'] == 'success':
        # print("ok",len( res['feature']))
        print("ok", res['data'])

def get_task(server_ip,url,params=''):
    url = "http://" + server_ip + ":80/" + url+params
    print(url)

    # headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    response = requests.get(url)#, headers=headers)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)
    result = json.loads(response.text)
    if result['returnCode']=='0' and result['usedNum']>0:
        for taskId in result['taskIds']:
            print(taskId)
        return result['taskIds']
    else:
        print("no task")
        return []

def del_task(server_ip,url,taskID=''):
    url = "http://" + server_ip + ":80/" + url + taskID
    body = {"taskID": taskID}
    response = requests.post(url,json.dumps(body))  # , headers=headers)
    print(response.text)
    res = json.loads(response.text)
    if res['returnCode'] == '0':
        print("del ok")
    # 返回信息
    return res
if __name__ == '__main__':
    server_ip = "192.168.55.120"
    # create()
    result = get_task(server_ip, url="Task/QueryResource?ProjectID=1000")
    for taskID in result:
        pass
        result = del_task(server_ip, url="Task/DeleteTask", taskID=taskID)
    # get_task(server_ip, url="Task/QueryResource?ProjectID=1000")

