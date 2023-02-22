#!/usr/bin/env python
# coding: utf-8
# Author : EnGuang
from Crypto.Cipher import AES
import base64
import json


def is_json(data):
    try:
        json.loads(data)
    except Exception as e:
        return False
    return True
# 获取数据中的目标字符串
def get_str(data):
    if '<' in data:
        value = data.split('<')[-1].split('>')[0]
        return value


# base64编码
def base64_en(cipher_text):
    encode_bytes = base64.b64encode(cipher_text.encode('utf-8'))
    encode_str = str(encode_bytes, 'utf-8')
    return encode_str


# base64解码
def base64_de(cipher_text):
    decode_bytes = base64.b64decode(cipher_text.encode('utf-8'))
    decode_str = str(decode_bytes, 'utf-8')
    return decode_str


# AES加密
def aes_encrypt(data):
    """使用PKCS7填充 """
    pad = lambda s :s+(16 - len(s)%16)*chr(16 - len(s)%16)
    # padding = length if (bytes_length == length) else bytes_length
    # padding = bs - padding_size % bs
    data = pad(data)
    """字符串补位 """
    key = '123456789qwertyasdfghjkl'.encode('utf-8')
    iv = 'aytrewq987654321'.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptedbytes = cipher.encrypt(data.encode('utf-8'))
    encodestrs = base64.b64encode(encryptedbytes)
    enctext = encodestrs.decode('utf-8')
    return enctext


# AES解密
def aes_decrypt(code_str):
    """使用PKCS7填充 """
    bs = 16
    length = len(code_str)
    bytes_length = len(code_str.encode('utf-8'))
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    coding = chr(padding)
    """使用CBC """
    key = '123456789qwertyasdfghjkl'.encode('utf-8')
    iv = 'aytrewq987654321'.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    content = base64.b64decode(code_str)
    text = cipher.decrypt(content).decode('utf-8')
    return text.rstrip(coding)
