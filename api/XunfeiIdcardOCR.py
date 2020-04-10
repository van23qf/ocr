#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    讯飞身份证OCR接口
    documents   https://www.xfyun.cn/doc/words/idCardRecg/API.html#%E6%8E%A5%E5%8F%A3%E8%BF%94%E5%9B%9E%E5%8F%82%E6%95%B0
"""

__author__ = 'Van23qf'


import requests
import time
import hashlib
import base64
import json

from system import global_dict


# 身份证识别接口接入地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/idcard"


def getHeader():
    api_config = global_dict.get_value("api_config")
    # 应用APPID（必须为webapi类型应用，并开通身份证识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481）
    APPID = api_config['appid']
    # 接口密钥（webapi类型应用开通身份证识别服务后，控制台--我的应用---身份证识别---相应服务的apikey）
    API_KEY = api_config['appsecret']
    curTime = str(int(time.time()))
    param = {"engine_type": "idcard", "head_portrait": "0"}
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


def ocr(file, side='front'):
    try:
        f1_base64 = str(base64.b64encode(file), 'utf-8')

        data = {
            'image': f1_base64
        }
        r = requests.post(URL, data=data, headers=getHeader())
        result = json.loads(str(r.content, 'utf-8'))
        if result['code'] != "0":
            return {'status': False, 'msg': result['code'] + '：' + result['desc']}
        if result['data']['error_code'] != 0:
            return {'status': False, 'msg': str(result['data']['error_code']) + '：' + result['data']['error_msg']}
        if result['data']['type'] != '第二代身份证背面' and result['data']['type'] != '第二代身份证' and result['data']['type'] != '身份证正反面或临时身份证':
            return {'status': False, 'msg': result['data']['type'] + '识别失败'}
        msg = 'success'
        if result['data']['type'] == '第二代身份证':
            return {
                'status': True,
                'msg': msg,
                'data': {
                    'side': 'front',
                    'name': result['data']['name'],
                    'gender': result['data']['sex'],
                    'nation': result['data']['people'],
                    'birth': result['data']['birthday'].replace('年', '-').replace('月', '-').replace('日', ''),
                    'address': result['data']['address'],
                    'idnum': result['data']['id_number'],
                }
            }
        elif result['data']['type'] == '身份证正反面或临时身份证':
            return {
                'status': True,
                'msg': msg,
                'data': {
                    'side': 'temp',
                    'name': result['data']['name'],
                    'gender': result['data']['sex'],
                    'nation': result['data']['people'],
                    'birth': result['data']['birthday'].replace('年', '-').replace('月', '-').replace('日', ''),
                    'address': result['data']['address'],
                    'idnum': result['data']['id_number'],
                    'authority': result['data']['issue_authority'],
                    'validity': result['data']['validity'],
                }
            }
        else:
            return {
                'status': True,
                'msg': msg,
                'data': {
                    'side': 'back',
                    'authority': result['data']['issue_authority'],
                    'validity': result['data']['validity'],
                }
            }
    except FileNotFoundError as err:
        return {'status': False, 'msg': err.strerror}


if __name__ == '__main__':
    result = ocr('../uploads/zhe.jpeg', 'front')
    print(result)

"""
{"code":"0","data":{"address":"湖北省红安县杏花乡嶂山村靠山店","birthday":"1992年6月23日","border_covered":false,"complete":true,"error_code":0,"error_msg":"OK","gray_image":false,"head_blurred":false,"head_covered":false,"id_number":"421122199206231036","issue_authority":"","name":"秦凡","people":"汉","sex":"男","time_cost":{"preprocess":148,"recognize":258},"type":"第二代身份证","validity":""},"desc":"success","sid":"wcr000602fc@gz88bb11707e81463000"}

"""