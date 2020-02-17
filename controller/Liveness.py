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
    project = request.form.get('project')
    file = base64.b64decode(request.form.get('file'))
    api_provider = request.form.get('api_provider')
    api_config = func.get_api_config('liveness', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    # file = func.read_file(file_name)
    # if not file:
    #     raise Exception('文件读取失败')
    if api_provider == 'faceid':
        result = FaceidLiveness.url(idcard_name, idcard_number, file)
    else:
        raise Exception('接口未知')
    return {'status': True, 'msg': 'success', 'data': {'url': result['url'], 'nonce_str': result['nonce_str']}}


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