#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang
import base64
import configparser
import json
import os
import random
import shutil
import string
from requests import post, put
from WriteLog import Logger
from web接口.common_api import base64_en, aes_encrypt


class DO:

    def init(self):
        cf = configparser.ConfigParser(allow_no_value=True)
        # self.path = os.getcwd()
        # self.con_path = self.path + 'config_face.ini'
        cf.read('config_face.ini', encoding="utf-8-sig")

        # 从配置文件中获取照片路径
        self.file_dict = cf.get("Photo_Path", "Photo_Path")
        self.code_msg = cf.get("Photo_Path", "code_msg")
        # print(self.code_msg)
        return self.file_dict,self.code_msg

    def PhotoToBase64(self,photopath):
        with open(photopath, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
            # print(image_base64)
            return image_base64

    def login(self,ip,pwd):
        body_ry = {"userName": "admin", "password": pwd}
        url = "http://" + ip + ":8090/api/user/login"
        res_ry = post(url=url, json=body_ry)
        r_ry = res_ry.json()
        sessionId = r_ry['data']['sessionId']
        return str(sessionId)

    def upload_file(self,sessionId, fi_d):
        if os.path.isfile(fi_d):  # 判断是否为一个文件
            with open(fi_d, 'rb') as f:
                image = f.read()
                size = len(image)  # 计算图片大小
                fi = os.path.basename(fi_d)
        # 上传图片
        url_upload = "http://" + ip + ":8090/api/upload/file"
        header = {"SessionId": sessionId}
        Query = {"type": "registerImage", "length": str(size)}
        files = {"paramfile": (fi, open(fi_d, "rb"), 'image/jpeg')}
        res_ry = post(url=url_upload, headers=header, params=Query, files=files)
        print(res_ry.json())
        return res_ry.json()['code']
        # print(res_ry.json())
        # if res_ry.json()['code'] == 0:
        #     cacheId = res_ry.json()['data']["cacheId"]
        #     return cacheId
        # else:
        #     cacheId =
        # except Exception as e:
        #     # print(res_ry.json())
        #     cacheId = ""
        #     return cacheId

    def trafficPerson(self,sessionId, name, cacheId):
        # 注册人员和照片
        id = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        personjson = {"personId": id, "name": name}
        body_ry = {"person": personjson, "face": [{"cacheId": cacheId, "registerId": id}], "finger": [],
                   "rule": [{"readerRule": {"ruleId": "DEVICEREADER"}, "timezoneRule": {"ruleId": "TIMEZONERULE"}}]}
        header = {"Content-Type": "application/json", "SessionId": sessionId}
        url_renyuan = "http://" + ip + ":8090/api/trafficPerson/info"
        res_ry = put(url=url_renyuan, headers=header, json=body_ry)
        r_ry = res_ry.json()
        return r_ry

    def Add_Person_and_Face(self,sessionId,Code,photo_path):
        # try:
            file_name = photo_path.split('\\')[-1].split('.')[0]
            code = self.upload_file(sessionId, photo_path)
            # res_ry = self.trafficPerson(sessionId, file_name, cacheId)
            if str(code) == str(Code):
                result = str(code) + ':该照片注册结果符合预期'
                return result
            else:
                result = str(code) + ":该照片注册结果不符合预期"
                # self.handle_photo(photo_path, folder_path)
                return result

        # except Exception as e:
        #     result = '出错了:'+str(e)
        #     return result

    def handle_photo(self,photo_path,folder_path):
        file_name = photo_path.split('\\')[-2]
        PATH = self.CreateFile(folder_path,file_name)
        shutil.copy(photo_path, PATH)

    def CreateFile(self,folder_path,filename):
        Photo_path = '%s\\%s' % (folder_path,filename)
        if not os.path.exists(Photo_path):
            os.mkdir(Photo_path)
        return Photo_path

    # def get_code(self):
    #     try:
    #         file_dict,code_msg = self.init()
    #         code_list = eval(file_dict).keys()
    #         return code_list
    #     except Exception as e:
    #         print(e)

    def main(self,ip, pwd):
        sessionId = self.login(ip, pwd)

        logger = Logger()
        logpath = logger.creatLog('register')

        file_dict, code_msg = DO().init()
        CodeList = eval(file_dict).keys()

        for code in CodeList:
            logger.get_log().info('开始添加该code对应的照片：' + code)
            FilePath = eval(file_dict)[code]
            logger.get_log().info('找到上述code:---' + code + '---对应的照片路径：' + FilePath)
            files_s = os.listdir(FilePath)  # 遍历目录下所有文件，包括子目录
            for files_ss in files_s:
                files_ss_path = os.path.join(FilePath, files_ss)  # 拼接路径
                if (files_ss.lower().endswith(
                        ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm',
                         '.tif', '.tiff'))):  # 判断是否为一个照片文件
                    logger.get_log().info('开始注册该照片：' + files_ss_path)

                    face_result = self.Add_Person_and_Face(sessionId, code, files_ss_path)
                    logger.get_log().info(face_result)
                elif (files_ss.lower().endswith(('.db'))):  # 判断是否为一个db文件:
                    # print('不是照片，不进行注册')
                    pass
                else:
                    files_sss = os.listdir(files_ss_path)  # 遍历子目录下所有文件，包括子目录
                    for files_ssss in files_sss:
                        files_ssss_path = os.path.join(files_ss_path, files_ssss)  # 拼接路径
                        if (files_ssss_path.lower().endswith(('.db'))):  # 判断是否为一个db文件:
                            # print('不是照片，不进行注册')
                            pass
                        else :
                            logger.get_log().info('开始注册该照片：' + files_ssss_path)
                            face_result1 = self.Add_Person_and_Face(sessionId,code,files_ssss_path)
                            logger.get_log().info(face_result1)

        print('日志路径：' + logpath)
        print("-------------注册测试-执行完成--------------")


if __name__ == '__main__':
    ip = '192.168.41.234'
    pwd = '1111aaaa'
    pwd = base64_en(aes_encrypt(pwd))
    DO().main(ip, pwd)




