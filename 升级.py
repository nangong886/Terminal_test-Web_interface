#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang

import os
import time
from requests_toolbelt.multipart import encoder
from common_api import base64_en, aes_encrypt
from requests import post, put, get
import hashlib
pwd = '1111aaaa'    # 设备密码
ip = '192.168.42.120'    # 设备ip
pwd = base64_en(aes_encrypt(pwd))
package_address1 = r'\\192.168.1.8\终端产品部固件版本管理\Linux\基线\rv1109\Debug\TGD\TGD-V2.2297\SAC_TGD-V2.2297_221130.tar.gz'
package_address2 = r'\\192.168.1.8\终端产品部固件版本管理\Linux\基线\rv1109\Debug\TGD\TGD-V204.2203\SAC_TGD-V204.2203_221026.tar.gz'
times = 500


# 文件上传进度
def upload_monitor(monitor):
    pass
    # print(round(monitor.bytes_read/monitor.len*100,2))


# 登录获取sessionId
def login():
    body_ry = {"userName":"admin","password":pwd}
    url = "http://" + ip + ":8090/api/user/login"
    res_ry = post(url=url, json=body_ry)
    r_ry = res_ry.json()
    sessionId = r_ry['data']['sessionId']
    return str(sessionId)


# 升级
def startUpgrade(sessionId,package_address):
    try:
        if os.path.isfile(package_address):  # 判断是否为一个文件
            with open(package_address, 'rb') as f:
                package = f.read()
                size = len(package)  # 计算图片大小
                fi = os.path.basename(package_address)    # 文件名

        # 校验MD5
        url = "http://" + ip + ":8090/api/system/startUpgrade"
        Query = {"name": fi, "type": "system", "length": str(size)}
        with open(package_address, 'rb') as f:
            md5 = (hashlib.md5(f.read()).hexdigest())
        body = {"md5": md5}
        head = {'Content-Type': 'application/json', "SessionId": sessionId}
        res_ry = post(url=url, headers=head, params=Query, json=body)
        print(res_ry.json())

        # 上固件包
        url_upgrade = "http://" + ip + ":8090/api/upload/upgrade"
        headers = {"SessionId": sessionId}
        Query_upgrade = {"name": fi, "type": "system", "length": str(size)}
        # files = {"paramfile": (fi, open(package_address, "rb"))}
        multipart_encoder = encoder.MultipartEncoder(
            fields={
                # 'name': 'paramfile',
                'paramfile': (fi, open(package_address, 'rb'), 'application/gzip')  # 根据上传文件类型的不同而不同
            },
        )
        monitor = encoder.MultipartEncoderMonitor(multipart_encoder, upload_monitor)
        # print(multipart_encoder.content_type)
        headers['Content-Type'] = multipart_encoder.content_type
        # print(headers)
        res_ry = post(url_upgrade,params=Query_upgrade, data=monitor, headers=headers)
        print(res_ry.json())

    except Exception as e:
        print(e)


def get_device_info(sessionId):
    url = "http://%s:8090/api/system/deviceInfo" % (ip)
    head = {"Content-Type": "application/json", "SessionId": str(sessionId)}
    res_ry = get(url=url, headers=head)
    # print(res_ry.json())
    appVersion = res_ry.json()['data']['appVersion']
    return appVersion


def main(package_address1,package_address2):
    timestamp = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
    print(timestamp)
    sessionId = login()
    startUpgrade(sessionId, package_address1)
    time.sleep(300)
    sessionId = login()
    appVersion = get_device_info(sessionId)
    if appVersion == (os.path.basename(package_address1)).split('_')[1]:
        print(appVersion+'升级成功')

    timestamp = time.strftime('%Y%m%d %H:%M:%S', time.localtime())
    print(timestamp)
    sessionId = login()
    startUpgrade(sessionId, package_address2)
    time.sleep(300)
    sessionId = login()
    appVersion = get_device_info(sessionId)
    if appVersion == (os.path.basename(package_address2)).split('_')[1]:
        print(appVersion + '升级成功')


if __name__ == '__main__':
    i = 0
    while i< times:
        print('---------第' + str(i + 1) + '次测试----------')
        main(package_address1, package_address2)
        i= i+1





