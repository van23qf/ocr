#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import requests
import json
import hashlib
from flask import Flask, request
import config
from system import func


OCR_API_CONFIG = {
    'api_key': config.faceid['idcard']['api_key'],
    'api_secret': config.faceid['idcard']['api_secret']
}


def get_randstr(len):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    return ''.join(sa)


def get_token(idcard_name, idcard_number, **kw):
    data = {
        'api_key': OCR_API_CONFIG['api_key'],
        'api_secret': OCR_API_CONFIG['api_secret'],
        'comparison_type': "1",
        'idcard_name': idcard_name,
        'idcard_number': idcard_number,
        'return_url': 'https://www.qfcoder.com/open/faceid',
        'notify_url': 'https://www.qfcoder.com/open/faceid',
        'biz_no': get_randstr(10),
        'biz_extra_data': '',
    }
    image_file = {}
    if kw.get('image_ref1'):
        image_file['image_ref1'] = kw.get('image_ref1')
    if kw.get('image_ref2'):
        image_file['image_ref2'] = kw.get('image_ref2')
    if kw.get('image_ref3'):
        image_file['image_ref3'] = kw.get('image_ref3')
    response = requests.post('https://api.megvii.com/faceid/liveness/v2/get_token', data=data, files=image_file)
    result = json.loads(response.text)
    if not result.get('token'):
        raise Exception('token获取失败')
    return result['token']


def url(idcard_name, idcard_number, face_pic):
    token = get_token(idcard_name, idcard_number, image_ref1=face_pic)
    return 'https://api.megvii.com/faceid/liveness/v2/do?token=' + token


def callback():
    data_json = request.form.get('data')
    outsign = request.form.get('sign')
    sign_str = OCR_API_CONFIG['api_secret'] + data_json
    sign = hashlib.sha1(sign_str.encode("utf-8")).hexdigest()
    if sign != outsign:
        raise Exception('签名错误')
    data = json.loads(data_json)
    # 活体检测结果
    if data['liveness_result']['result'] != 'success':
        failure_reason = data['liveness_result']['result']
        if failure_reason.get('action_mixed'):
            raise Exception('做了错误的动作')
        elif failure_reason.get('not_video'):
            raise Exception('检测到活体攻击')
        elif failure_reason.get('timeout'):
            raise Exception('活体动作超时')
        elif failure_reason.get('quality_check_timeout'):
            raise Exception('照镜子流程超时（120秒）')
        elif failure_reason.get('no_input_frame'):
            raise Exception('视频流输入中断')
        elif failure_reason.get('interrupt_in_mirro_state'):
            raise Exception('用户在照镜子流程中断了网页端活体检测')
        elif failure_reason.get('interrupt_in_action_state'):
            raise Exception('用户在活体做动作时中断了网页端活体检测')
        else:
            raise Exception('活体检测结果未知')
    return True


if __name__ == '__main__':
    print(url('秦凡', '421122199206231036', func.read_file('../uploads/idcard_front.jpg')))
#{'time_used': 1674, 'token': '73ad30686686f19698939188c3a8c0b3', 'expired_time': 1580786981, 'request_id': '1580783979,1b16a332-05ad-47d7-aa48-7931e8c9d6a2'}
