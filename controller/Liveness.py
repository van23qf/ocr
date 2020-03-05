#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request
import base64, json
from api import FaceidLiveness

from system import func
from system import global_dict
from system import db


def url():
    idcard_name = request.form.get('idcard_name')
    idcard_number = request.form.get('idcard_number')
    return_url = request.form.get('return_url')
    project = request.headers.get('Project-Name')
    file = base64.b64decode(request.form.get('file'))
    api_provider = request.form.get('api_provider')
    if not api_provider or not file or not project or not idcard_name or not idcard_number:
        raise Exception('参数不全')
    api_config = func.get_api_config('liveness', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    # file = func.read_file(file_name)
    # if not file:
    #     raise Exception('文件读取失败')
    if api_provider == 'faceid':
        result = FaceidLiveness.url(idcard_name, idcard_number, file, return_url)
    else:
        raise Exception('接口未知')
    return {'status': True, 'msg': 'success', 'data': {'url': result['url'], 'nonce_str': result['nonce_str']}}


def compare():
    project = request.headers.get('Project-Name')
    image1 = base64.b64decode(request.form.get('image1'))
    image2 = base64.b64decode(request.form.get('image2'))
    api_provider = request.form.get('api_provider')
    if not api_provider or not project or not image1 or not image2:
        raise Exception('参数不全')
    api_config = func.get_api_config('compare', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    # file = func.read_file(file_name)
    # if not file:
    #     raise Exception('文件读取失败')
    if api_provider == 'faceid':
        result = FaceidLiveness.compare(image1, image2)
    else:
        raise Exception('接口未知')
    func.save_api_log('compare', json.dumps(result), project, api_provider)
    return result


def result_check():
    nonce_str = request.form.get('nonce_str')
    if not nonce_str:
        raise Exception('参数错误')
    sql = "select * from liveness_callback where nonce_str='{nonce_str}'".format(nonce_str=nonce_str)
    result = db.get_one(sql)
    if not result:
        raise Exception('不存在的nonce_str')
    if result['check_status'] != 1:
        raise Exception('检测失败')
    return {'status': True, 'msg': 'success'}


def faceid_callback():
    project = request.args.get('project')
    api_provider = request.args.get('api_provider')
    api_config = func.get_api_config('liveness', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    return FaceidLiveness.callback()