

import time
import threading

start=time.time()
aaaa={}
aaaa["adf"] = time.time()


def f1(a1, a2):
    global aaaa
    for i in range(200):
        time1 = time.time() - aaaa["adf"]
        if time1 > 1:
            print("di di")
            aaaa["adf"] = time.time()
        time.sleep(0.1)

if __name__ == '__main__':

    '''下面代码是直接运行下去的，不会等待函数里面设定的sleep'''
    t = threading.Thread(target=f1, args=(111, 112))  # 创建线程
    # t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    t.start()  # 开启线程