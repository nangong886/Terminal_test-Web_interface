#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang

import random
import string
import time
from common_api import base64_en, aes_encrypt
from requests import post, put
import os

file_path = r'\\192.168.1.8\qa\算法测试照片库\全公司人员20210701'    # 照片地址
pwd = '1111aaaa'    # 设备密码
ip = '192.168.42.95'    # 设备ip
pwd = base64_en(aes_encrypt(pwd))


def login():
    body_ry = {"userName":"admin","password":pwd}
    url = "http://" + ip + ":8090/api/user/login"
    res_ry = post(url=url, json=body_ry)
    r_ry = res_ry.json()
    sessionId = r_ry['data']['sessionId']
    return str(sessionId)


def upload_file(sessionId,fi_d):
    try:
        if os.path.isfile(fi_d):  # 判断是否为一个文件
            with open(fi_d, 'rb') as f:
                image = f.read()
                size = len(image)  # 计算图片大小
                fi = os.path.basename(fi_d)
        # 上传图片
        url_upload ="http://" + ip + ":8090/api/upload/file"
        header = {"SessionId": sessionId}
        Query = {"type":"registerImage","length":str(size)}
        files = {"paramfile": (fi, open(fi_d, "rb"), 'image/jpeg')}
        res_ry = post(url=url_upload, headers=header, params=Query, files = files)
        # print(res_ry.json())
        cacheId = res_ry.json()['data']["cacheId"]
        return cacheId
    except Exception as e:
        # print(res_ry.json())
        cacheId = ""
        return cacheId


def trafficPerson(sessionId,name,cacheId):
    # 注册人员和照片
    id = ''.join(random.sample(string.ascii_letters + string.digits, 30))
    personjson = {"personId": id,  "name":  name}
    body_ry = {"person": personjson, "face": [{"cacheId":cacheId,"registerId":id}],"finger": [],"rule":[{"readerRule":{"ruleId":"DEVICEREADER"},"timezoneRule":{"ruleId":"TIMEZONERULE"}}]}
    header = {"Content-Type": "application/json", "SessionId": sessionId}
    url_renyuan = "http://" + ip + ":8090/api/trafficPerson/info"
    res_ry = put(url=url_renyuan, headers=header, json=body_ry)
    r_ry = res_ry.json()
    print(r_ry)


def run_registed(file_path):
    timestamp = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
    print('开始执行:' + timestamp)
    sessionId = login()
    files = os.listdir(file_path)  # 遍历file_path下所有文件，包括子目录
    i = 0
    for fi in files:
        print(str(fi))
        name = fi.split('.')[0]  # 照片名作为人员姓名
        fi_d = os.path.join(file_path, fi)
        timestamp1 = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
        print('第' + str(i) + '次:' + timestamp1)
        cacheId = upload_file(sessionId, fi_d)
        if cacheId == 0:
            pass
        else:
            trafficPerson(sessionId, name, cacheId)
            i = i+1


if __name__ == '__main__':
    run_registed(file_path)
