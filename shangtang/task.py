# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

def task_create(server_ip,url, dbName,call_ip,video_path):
    url="http://"+server_ip+":80/"+url
    body = {}
    body["taskType"] = 0  # , // 任务类型固定填 0
    body["param"] = {}
    body["param"]["Source"] = {}
    body["param"]["Source"]["SourceType"] = 2
    body["param"]["Source"]["RtspUrl"] = video_path
    body["param"]["Source"]["ProtoType"] = 0
    body["param"]["Result"] = []
    body["param"]["Result"].append({"Index": 0, "ProtocolType": 10, "URL": call_ip, "FilterNoImg": 1})
    body["param"]["Result"].append({"Index": 1, "ProtocolType": 10, "URL": call_ip, "FilterNoImg": 1})
    body["param"]["Private"]={}
    body["param"]["Private"]["targets"]=[]
    body["param"]["Private"]["targets"].append({"dbId": dbName, "score": 0.3})

    print( json.dumps(body))
    response = requests.post(url, json.dumps(body))
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    if response.status_code==404:
        print("error 404")
        return response.text
    res=json.loads(response.text)
    # 返回信息
    return res
if __name__ == '__main__':
    server_ip = "192.168.55.120"

    call_ip= "192.168.25.68:8888"
    # get_db(server_ip,url="verify/target/gets")

    path="rtsp://admin:sbdwl123@192.168.25.41:554/h264/ch1/main/av_stream"
    # path="rtsp://admin:sbdwl123@192.168.25.45:554/h264/ch1/main/av_stream"
    res=task_create(server_ip,url="Task/CreateTask?ProjectID=1000",dbName="sbd_test01",call_ip=call_ip,video_path=path)
    print(res)
    if '<html>'in res:
        print("error")
    elif res['returnCode'] == 0:
       print(res['taskID'])

    elif res['returnCode'] == 'success':
        # print("ok",len( res['feature']))
        print("ok", res['data'])
