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


# 查询人员列表，并列出所有人的personID
def trafficPerson(sessionId):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    body_ry = {"page": {"pageNum": 1, "limit": 30}}
    url = "http://" + ip + ":8090/api/trafficPerson/list"
    res_ry = post(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    # print(r_ry)
    if r_ry['code'] == 0:
        person_ids = []  # 如果响应体r_ry中code为0，定义一个列表变量person_ids
        if r_ry["data"]["total"] > 0:
            datas = r_ry["data"]["list"]  # 且如果响应体中data的total数大于0，则获取data的list并赋值为datas
            for list in datas:
                person_ids.append(list["person"]["personId"])  # 循环取人员信息的人员Id放到datas列表
                # print(person["personId"])
        return person_ids
    else:
        print('查询失败')


# 根据查出的人员personId做删除
def deletePerson(sessionId, personId):
    head = {"Content-Type": "application/json", "SessionId": sessionId}
    body_ry = {"personId": personId}
    url = "http://" + ip + ":8090/api/trafficPerson/info"
    res_ry = delete(url=url, headers=head, json=body_ry)
    r_ry = res_ry.json()
    if r_ry['code'] == 0:
        print('调用删除接口成功')
    else:
        print('删除失败')


if __name__ == '__main__':
    session_id = login()
    person_ids = trafficPerson(session_id)
    if len(person_ids) == 0:
        person_id = []
        print("人员列表为空")  # 容错处理：如果列表person_ids为空时，再定义一个列表变量person_id（里面是预备删除的人员），并打印人员列表为空
    else:
        person_id = [person_ids[0]]
    deletePerson(session_id, person_id)  # 否则不为空时，取列表person_ids中的第一个并赋值给列表person_id，最终执行删除方法
