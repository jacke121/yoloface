# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from io import BytesIO

import requests
import json
import global_var_model as gl_var
def search_pic(server_ip, dbName,path):
    url = 'verify/face/search'
    url="http://"+server_ip+":9001/"+url
    body = {"dbName":dbName,"topNum":6,"score":'0.7'}

    # 原来写的是 img=[('imageData', (path, open(path,'rb')))]
    with open(path,'rb') as f:
        imagedata=f.read()
    img={'imageData':imagedata}
    response = requests.post(url, body,files=img)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    res=json.loads(response.text)
    if res['result'] == "error":
        if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
            print(1)
        elif 'NO_FACE_DETECTED' in res['errorMessage']:
            pass
        else:
            print("error", res['errorMessage'])
    elif res['result'] == 'success':
        print('quality', res["quality"])
        if len(res["data"]) == 0:
            return None
        data = res["data"][0]
        if float(data["score"]) < 0.7:
            print("find no similar", data["score"])
            return None
        data["user_idx"] = data["imageId"]
        return data
def search_pic_by_url(server_ip,dbName,name,img_src):
    url = 'verify/face/search'
    url = "http://" + server_ip + ":9001/" + url
    body = {"dbName": dbName, "topNum": 6, "score": '0.7'}
    # img = [('imageData', (path, open(path, 'rb')))]
    response = requests.get(img_src)
    bytes = BytesIO(response.content)
    img={'imageData': (name, bytes)}
    rsp = requests.post(url, body, files=img)
    if rsp.status_code!=200:
        print("search_pic_by_url status",rsp.status_code)
        return None
    try:
      res=json.loads(rsp.text)
    except Exception as e:
        print("search_pic_by_url",e)
    if res['result'] == "error":
        print("error", res['errorMessage'])
        return None
    elif res['result'] == 'success':
        if len(res["data"])==0:
            return None
        print('quality',res["quality"])
        data=res["data"][0]
        if float(data["score"])<0.7:
            print("find no similar",data["score"])
            return None
        data["user_idx"]=data["imageId"]
        return data

def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list

def query_path():
    path=r'D:\project\face\face_detect\sht_face'

    for img in get_file_list(path):
        res = search_pic(gl_var.camera_server_ip, dbName="sbd_db02",
                         path=path+'/'+img)
        print(img,res)


if __name__ == '__main__':
    query_path()
    server_ip = "192.168.55.120"
    # get_db(server_ip,url="verify/target/gets")

    # res = search_pic(gl_var.camera_server_ip, dbName="sbd_db02", path=r'D:\project\face\face_detect\sht_face\31.jpg')
    # print(res)

    # name="lixiao"
    # path = "d:/f1.jpg"
    # res=search_pic(server_ip,dbName="sbd_db02",path=r'D:\project\flask_server\monitor\static\upload\avatar\2018-10-28/v2_cf05287b33e1d639feeb396f455096b641a04ff5.jpg')
    # res=search_pic_by_url(server_ip=server_ip, dbName=gl_var.dbname, name='default', img_src=r'http://192.168.55.120:18080/g1/M00/00/00/rBIAFFvUDBeIQczyAABrE5SzdccAAAAQQNgizAAAGsr798.jpg')
    # res=search_pic_by_url(server_ip=server_ip, dbName=gl_var.dbname, name='default', img_src=r'http://192.168.55.120:18080/g1/M00/00/00/rBIAFFvVeoyIEdzhAABavu3geloAAAASQSXvq4AAFrW035.jpg')
    # res=search_pic_by_url(server_ip=server_ip, dbName=gl_var.dbname, name='default', img_src=r'http://192.168.55.120:18080/g1/M01/00/00/rBIAFFvVlQiIZ-A1AABKQAi6YFQAAAASgD-YlQAAEpY395.jpg')
    # print(res)

    # src = "http://192.168.55.120:18080/g1/M01/00/00/rBIAFFvRgwuIF8oUAABc4QuieokAAAANAZpojsAAFz5189.jpg"
    # data=search_pic_by_url(server_ip,url="verify/face/search",dbName="sbd_sbd02",name="name",img_src=src)
    # if data:
    #     print(data)
    # res = create_db(server_ip, url="verify/target/deletes", params="?dbName=aaa4")
    # if res['result'] == "error":
    #     if "FAILED_TO_CREATE_DB_EXISTS" == res['errorMessage']:
    #         print(1)
    #     print("error", res['errorMessage'])
    # elif res['result'] == 'success':
    #     print("ok", res['data'])