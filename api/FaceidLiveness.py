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


def compare(image1, image2, **kw):
    api_config = global_dict.get_value("api_config")
    nonce_str = get_randstr(16)
    data = {
        'sign': make_sign(api_config['appid'], api_config['appsecret']),
        'sign_version': "hmac_sha1",
        'liveness_type': "raw_image",
        'comparison_type': "0",
        'uuid': nonce_str,
        'multi_oriented_detection': '1',
        'biz_no': nonce_str,
        'biz_extra_data': '',
    }
    image_file = {
        'image': image1,# 待对比的人脸照片
        'image_ref1': image2,
    }
    response = requests.post('https://api.megvii.com/faceid/v3/sdk/get_biz_token', data=data, files=image_file)
    result = json.loads(response.text)
    if result.get('error'):
        raise Exception(result.get('error'))
    # 拿到biz_token，做验证
    biz_token = result['biz_token']
    vdata = {
        'sign': make_sign(api_config['appid'], api_config['appsecret']),
        'sign_version': "hmac_sha1",
        'biz_token': biz_token,
    }
    vresponse = requests.post('https://api.megvii.com/faceid/v3/sdk/verify', data=vdata)
    vresult = json.loads(vresponse.text)
    if vresult.get('error'):
        raise Exception(vresult.get('error'))
    if vresult['result_code'] >= 1000 and vresult['result_code'] < 3000:
        return {'status': True, 'msg': 'success'}
    if vresult['result_code'] >= 3000 and vresult['result_code'] < 3100:
        raise Exception(vresult['result_code'])
    if vresult['result_code'] >= 3100 and vresult['result_code'] < 4000:
        raise Exception('参考数据调用出错')
    if vresult['result_code'] >= 4000 and vresult['result_code'] < 4100:
        raise Exception(vresult['result_code'])
    if vresult['result_code'] >= 4100 and vresult['result_code'] < 4200:
        raise Exception('云端活体判断未通过')
    if vresult['result_code'] >= 4200 and vresult['result_code'] < 4300:
        raise Exception('SDK活体图像采集失败')
    raise Exception('验证失败')


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
    api_config = {
        'project': 'papv2.local',
        'api_provider': 'faceid',
        'appid': 'rlN7N8CiT77yls3RuxrqtKGx7rv6JW66',
        'appsecret': '5OagY6r_PQYdtX3tMczjPCkAm4dneVkq',
    }
    print(compare(func.read_file('../uploads/1.jpg'), func.read_file('../uploads/idcard_front.jpg')))
    # https://api.megvii.com/faceid/lite/do?token=7166b782b290f4d20621795267de9c92
    #print(url('秦凡', '421122199206231036', func.read_file('../uploads/idcard_front.jpg')))
#{'time_used': 1674, 'token': '73ad30686686f19698939188c3a8c0b3', 'expired_time': 1580786981, 'request_id': '1580783979,1b16a332-05ad-47d7-aa48-7931e8c9d6a2'}
