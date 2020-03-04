#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random
import requests
import json
import hashlib
from datetime import datetime
from flask import Flask, request
from system import global_dict
from system import func
from config import config
from system.model import LivenessCallback


def get_randstr(len):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(len):
        sa.append(random.choice(seed))
    return ''.join(sa)


def get_token(idcard_name, idcard_number, **kw):
    api_config = global_dict.get_value("api_config")
    nonce_str = get_randstr(16)
    data = {
        'api_key': api_config['appid'],
        'api_secret': api_config['appsecret'],
        'comparison_type': "1",
        'idcard_name': idcard_name,
        'idcard_number': idcard_number,
        'return_url': kw.get('return_url'),
        'notify_url': 'http://{host}/liveness/faceid/callback?project={project}&api_provider={api_provider}'.format(host=config.server_name, project=api_config['project'], api_provider=api_config['api_provider']),
        'biz_no': nonce_str,
        'biz_extra_data': '',
    }
    image_file = {}
    if kw.get('image_ref1'):
        image_file['image_ref1'] = kw.get('image_ref1')
    if kw.get('image_ref2'):
        image_file['image_ref2'] = kw.get('image_ref2')
    if kw.get('image_ref3'):
        image_file['image_ref3'] = kw.get('image_ref3')
    #response = requests.post('https://api.megvii.com/faceid/liveness/v2/get_token', data=data, files=image_file)
    response = requests.post('https://api.megvii.com/faceid/lite/get_token', data=data, files=image_file)
    result = json.loads(response.text)
    log_id = func.save_api_log('liveness', json.dumps(result), api_config['project'], api_config['api_provider'], nonce_str)
    if not result.get('token'):
        print(data)
        raise Exception('token获取失败')
    return {'token': result['token'], 'log_id': log_id, 'nonce_str': nonce_str}


def url(idcard_name, idcard_number, file, return_url):
    result = get_token(idcard_name, idcard_number, image_ref1=file, return_url=return_url)
    #url = 'https://api.megvii.com/faceid/liveness/v2/do?token=' + result['token']
    url = 'https://api.megvii.com/faceid/lite/do?token=' + result['token']
    return {'url': url, 'nonce_str': result['nonce_str']}


def callback():
    api_config = global_dict.get_value("api_config")
    data_json = request.form.get('data')
    outsign = request.form.get('sign')
    sign_str = api_config['appsecret'] + data_json
    sign = hashlib.sha1(sign_str.encode("utf-8")).hexdigest()
    data = json.loads(data_json)
    nonce_str = data['biz_no']
    liveness_callback = LivenessCallback.Model()
    liveness_callback.nonce_str = nonce_str
    liveness_callback.result = data_json
    liveness_callback.created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if sign != outsign:
        raise Exception('签名错误')
    # 活体检测结果
    liveness_result_fail = None
    if data['liveness_result']['result'] != 'success':
        failure_reason = data['liveness_result']['result']
        if failure_reason.get('action_mixed'):
            liveness_result_fail = '做了错误的动作'
        elif failure_reason.get('not_video'):
            liveness_result_fail = '检测到活体攻击'
        elif failure_reason.get('timeout'):
            liveness_result_fail = '活体动作超时'
        elif failure_reason.get('quality_check_timeout'):
            liveness_result_fail = '照镜子流程超时（120秒）'
        elif failure_reason.get('no_input_frame'):
            liveness_result_fail = '视频流输入中断'
        elif failure_reason.get('interrupt_in_mirro_state'):
            liveness_result_fail = '用户在照镜子流程中断了网页端活体检测'
        elif failure_reason.get('interrupt_in_action_state'):
            liveness_result_fail = '用户在活体做动作时中断了网页端活体检测'
        else:
            liveness_result_fail = '活体检测结果未知'
    if liveness_result_fail:
        liveness_callback.check_status = 0
    liveness_callback.check_status = 1
    liveness_callback.insert()
    return {'status': True, 'msg': 'success'}


if __name__ == '__main__':
    print(url('秦凡', '421122199206231036', func.read_file('../uploads/idcard_front.jpg')))
#{'time_used': 1674, 'token': '73ad30686686f19698939188c3a8c0b3', 'expired_time': 1580786981, 'request_id': '1580783979,1b16a332-05ad-47d7-aa48-7931e8c9d6a2'}
