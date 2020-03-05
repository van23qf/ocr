#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
import base64, json
from api import TencentVerify, FaceidVerify

from system import func
from system import global_dict

def index():
    idcard_name = request.form.get('idcard_name')
    idcard_number = request.form.get('idcard_number')
    project = request.headers.get('Project-Name')
    api_provider = request.form.get('api_provider')
    if not idcard_name or not idcard_number or not api_provider or not project:
        raise Exception('参数不全')
    api_config = func.get_api_config('idcard', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    # file = func.read_file(file_name)
    # if not file:
    #     raise Exception('文件读取失败')
    if api_provider == 'tencent':
        result = TencentVerify.check(idcard_name, idcard_number)
    elif api_provider == 'faceid':
        result = FaceidVerify.check(idcard_name, idcard_number)
    else:
        raise Exception('接口未知')
    func.save_api_log('verify', json.dumps(result), project, api_provider)
    return result