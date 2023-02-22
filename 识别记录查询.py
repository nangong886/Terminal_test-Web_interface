#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang

import random
import string
import time
from common_api import base64_en, aes_encrypt
from requests import post, put

pwd = '1'    # 设备密码
ip = '192.168.40.198'    # 设备ip
pwd = base64_en(aes_encrypt(pwd))
times = 1000


def login():
    body_ry = {"userName":"admin","password":pwd}
    url = "http://" + ip + ":8090/api/user/login"
    res_ry = post(url=url, json=body_ry)
    r_ry = res_ry.json()
    sessionId = r_ry['data']['sessionId']
    return str(sessionId)


def recordList(sessionId):
    head = {"Content-Type": "application/json","SessionId":sessionId}
    body_ry = {"type":1,"sort":"false","page":{"pageNum":1,"limit":30}}
    url = "http://" + ip + ":8090/api/identify/recordList"
    res_ry = post(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    if r_ry['code'] == 0:
        print('查询成功')
    else:
        print('查询失败')


if __name__ == '__main__':
    sessionId = login()
    i = 0
    while i<times:
        print('---------第'+str(i+1)+'次查询----------')
        recordList(sessionId)
        i = i+1

