#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang
import time

from common_api import base64_en, aes_encrypt
from requests import post, put, get
import random
import string

pwd = '1111aaaa'    # 设备密码
ip = '192.168.43.237'    # 设备ip
pwd = base64_en(aes_encrypt(pwd))
times = 10000


def login():
    body_ry = {"userName":"admin","password":pwd}
    url = "http://" + ip + ":8090/api/user/login"
    res_ry = post(url=url, json=body_ry)
    r_ry = res_ry.json()
    print(r_ry)
    sessionId = r_ry['data']['sessionId']
    return str(sessionId)


# 调用刷卡注册
def startRegister(sessionId,id):
    head = {"Content-Type": "application/json","SessionId":sessionId}
    body_ry = {"type":1,"timeout":60,"person":{"personId":id,"name": id}}
    url = "http://" + ip + ":8090/api/trafficPerson/startRegister"
    res_ry = post(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    if r_ry['code'] == 0:
        print('调用刷卡注册成功')
    else:
        print('调用刷卡注册成功')


# 获取刷卡注册的卡号
def registerStatus(sessionId):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    url = "http://" + ip + ":8090/api/trafficPerson/registerStatus"
    res_ry = get(url=url, headers=head)
    r_ry = res_ry.json()
    if r_ry['data']['status'] == 'continue':
        cardNo = 0
    else:
        cardNo = r_ry['data']['cardNo']
    return cardNo


def cancelRegister(sessionId):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    body_ry = {"TYPE":1}
    url = "http://" + ip + ":8090/api/trafficPerson/cancelRegister"
    res_ry = post(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()


def trafficPerson_info(sessionId,id,cardNo):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    body_ry = {"person":{"empNo":id,"name":id,"cardNo":cardNo,"personId":id,"remoteId":""},"face":[],"finger":[],"rule":[{"readerRule":{"ruleId":"DEVICEREADER"},"timezoneRule":{"ruleId":"TIMEZONERULE"}}]}
    url = "http://" + ip + ":8090/api/trafficPerson/info"
    res_ry = put(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    # print(r_ry)
    if r_ry['code'] == 0:
        print('人员注册成功')
    else:
        print('人员注册失败')


if __name__ == '__main__':
    sessionId = login()
    i = 0
    while i < times:
        print('---------第'+str(i+1)+'次注册----------')
        id = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        startRegister(sessionId,id)
        time.sleep(5)
        cardNo = registerStatus(sessionId)
        cancelRegister(sessionId)
        trafficPerson_info(sessionId, id, cardNo)
        i = i+1


