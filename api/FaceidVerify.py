#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import requests
import json
import hashlib
import time
import random
import hmac
import base64
from datetime import datetime
from flask import Flask, request
from system import global_dict
from system import func
from config import config
from system.model import LivenessCallback

import env

def get_randstr(len):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    return ''.join(sa)


def make_sign(api_key, api_secret):
    valid_durtion = 100  # 有效时间100秒
    current_time = int(time.time())
    expire_time = current_time + valid_durtion
    rdm = ''.join(random.choice("0123456789") for i in range(10))
    raw = "a={}&b={}&c={}&d={}".format(api_key, expire_time, current_time, rdm)
    sign_tmp = hmac.new(func.str_to_bytes(api_secret), func.str_to_bytes(raw), hashlib.sha1).digest()
    return base64.b64encode(sign_tmp + func.str_to_bytes(raw))


def check(idcard_name, idcard_number):
    api_config = global_dict.get_value("api_config")
    data = {
        'api_key': api_config['appid'],
        'api_secret': api_config['appsecret'],
        'comparison_type': "1",
        'face_image_type': "raw_image",
        'idcard_name': idcard_name,
        'idcard_number': idcard_number,
    }
    image_file = {
        'image': func.read_file(env.root_path + "/api/avatar.png")
    }
    response = requests.post('https://api.megvii.com/faceid/v2/verify', data=data, files=image_file)
    result = json.loads(response.text)
    if result.get('error_message'):
        if result.get('error_message') == 'INVALID_NAME_FORMAT':
            raise Exception('当前姓名与身份证号码不匹配')
        elif result.get('error_message') == 'INVALID_IDCARD_NUMBER':
            raise Exception('当前姓名与身份证号码不匹配')
        elif result.get('error_message') == 'NO_SUCH_ID_NUMBER':
            raise Exception('身份证号码不存在')
        else:
            raise Exception(result.get('error_message'))
    return {'status': True, 'msg': 'success'}


if __name__ == '__main__':
    api_config = {
        'project': 'papv2.local',
        'api_provider': 'faceid',
        'appid': 'rlN7N8CiT77yls3RuxrqtKGx7rv6JW66',
        'appsecret': '5OagY6r_PQYdtX3tMczjPCkAm4dneVkq',
    }
    print(check('秦凡', '421122199206241036'))
"""
{'time_used': 673, 'id_exceptions': {'id_photo_monochrome': 0, 'id_attacked': 0}, 'result_faceid': {'confidence': 85.328, 'thresholds': {'1e-3': 62.169, '1e-5': 74.399, '1e-4': 69.315, '1e-6': 78.038}}, 'request_id': '1583397215,9aa334cc-8a4f-4c08-8a89-a1fd0707569a'}

"""