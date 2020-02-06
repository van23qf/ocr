#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    讯飞手写识别
"""

__author__ = 'Van23qf'


from urllib import parse
import base64
import hashlib
import time
import requests
import json
from json.decoder import JSONDecodeError


# OCR手写文字识别接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
# 应用APPID(必须为webapi类型应用,并开通手写文字识别服务,参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "5e08308b"
# 接口密钥(webapi类型应用开通手写文字识别后，控制台--我的应用---手写文字识别---相应服务的apikey)
API_KEY = "1f6e4f4e92619b27c704be5e413d7718"


def getHeader():
    curTime = str(int(time.time()))
    param = "{\"language\":\"cn|en\",\"location\":\"false\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    # 组装http请求头
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(filepath):
    with open(filepath, 'rb') as f:
        imgfile = f.read()
    data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
    return data


def ocr(pic):
    try:
        with open(pic, 'rb') as f:
            imgfile = f.read()
        data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
        r = requests.post(URL, headers=getHeader(), data=data)
        result = json.loads(str(r.content, 'utf-8'))
        if result['code'] != "0":
            return {'status': False, 'msg': result['code'] + '：' + result['desc']}
        data = []
        for v in result['data']['block']:
            if v['type'] == 'text':
                for v1 in v['line']:
                    for v2 in v1['word']:
                        data.append(v2['content'])
        return {'status': True, 'msg': 'success', 'data': data}
    except FileNotFoundError as err_file:
        return {'status': False, 'msg': err_file.strerror}
    except JSONDecodeError as json_err:
        return {'status': False, 'msg': "返回json数据格式错误"}


if __name__ == '__main__':
    result = ocr('../uploads/jibing.png')
    print(result)
