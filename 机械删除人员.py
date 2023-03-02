#!/usr/bin/env python
# coding: utf-8
# Author : NanGong

from common_api import base64_en, aes_encrypt
from requests import post, delete

pwd = 'test1234'  # 设备密码
ip = '192.168.43.132'  # 设备ip
pwd = base64_en(aes_encrypt(pwd))
times = 1000


# 登录
def login():
    body_ry = {"userName": "admin", "password": pwd}
    url = "http://" + ip + ":8090/api/user/login"
    res_ry = post(url=url, json=body_ry)
    r_ry = res_ry.json()
    # print(r_ry)
    sessionId = r_ry['data']['sessionId']
    return str(sessionId)


# 删除
def deletePerson(sessionId):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    personId = ['54a59cdfb89941c7a039ac3202bb02d1']
    body_ry = {"personId": personId}
    url = "http://" + ip + ":8090/api/trafficPerson/info"
    res_ry = delete(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    if r_ry['message'] == 'success':
        print('调用删除接口成功')
    else:
        print('删除失败')


if __name__ == '__main__':
    sessionId = login()
    deletePerson(sessionId)
