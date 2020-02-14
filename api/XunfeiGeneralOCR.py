#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    讯飞通用印刷体识别接口
    documents   https://www.xfyun.cn/doc/words/textRecg/API.html
"""

__author__ = 'Van23qf'


import requests
import time
import hashlib
import base64
import json

from config import config


# 印刷文字识别 webapi 接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
# 应用ID (必须为webapi类型应用，并印刷文字识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = config.xunfei['general']['appid']
# 接口密钥(webapi类型应用开通印刷文字识别服务后，控制台--我的应用---印刷文字识别---服务的apikey)
API_KEY = config.xunfei['general']['api_key']


def getHeader():
    #  当前时间戳
    curTime = str(int(time.time()))
    #  支持语言类型和是否开启位置定位(默认否)
    param = {"language": "cn|en", "location": "false"}
    param = json.dumps(param)
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64,'utf-8')
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


def ocr(file):
    try:
        f1_base64 = str(base64.b64encode(file), 'utf-8')
        data = {
            'image': f1_base64
        }
        r = requests.post(URL, data=data, headers=getHeader())
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


def xlc_table(data):
    try:
        result = {}
        result['title'] = data[1]
        result['name'] = data[4][2:5]
        result['sex'] = data[4][8:9]
        result['age'] = data[4][14:16]
        result['phone'] = data[4][20:31]
        result['idcard'] = data[5][5:]
        result['desease_date'] = data[6]
        return result
    except Exception as e:
        return False


if __name__ == '__main__':
    result = ocr('../uploads/111111.png')
    print(result)
