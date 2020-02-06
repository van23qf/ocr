#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    阿里云公章识别
    documents   https://help.aliyun.com/document_detail/91903.html
"""

__author__ = 'Van23qf'


import requests
import time
import hashlib
import base64
import json

import urllib, sys
import urllib.request
from urllib.error import URLError, HTTPError
from json.decoder import JSONDecodeError
import ssl


URL = 'https://stamp.market.alicloudapi.com/api/predict/ocr_official_seal'
APPCODE = '6dd4a3ccb5c6486e97646007c43aa653'


def ocr(file):
    try:
        with open(file, 'rb') as f:
            f1 = f.read()
        f1_base64 = str(base64.b64encode(f1), 'utf-8')
        bodys = {}
        bodys[''] = "{\"image\":\"" + f1_base64 + "\"}"
        post_data = bytes(bodys[''], encoding="utf-8")
        request = urllib.request.Request(URL, post_data)
        request.add_header('Authorization', 'APPCODE ' + APPCODE)
        # 根据API的要求，定义相对应的Content - Type
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(request, context=ctx)
        content = response.read()
        print(content)
        result = json.loads(content)
        if not result.get('result'):
            return {'status': False, 'msg': "返回数据错误"}
        data = []
        for v in result['result']:
            data.append(v['text']['content'])
        return {'status': True, 'msg': "success", 'data': data}
    except JSONDecodeError as json_err:
        return {'status': False, 'msg': "返回数据格式错误"}
    except HTTPError as http_err:
        return {'status': False, 'msg': str(http_err.code) + ":" + http_err.reason}
    except FileNotFoundError as err_file:
        return {'status': False, 'msg': err_file.strerror}


if __name__ == '__main__':
    result = ocr('../uploads/fapiao.png')
    print(result)
