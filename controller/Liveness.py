#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import Flask, request
import base64, json
from api import FaceidLiveness

from system import func
import global_dict


def url():
    idcard_name = request.form.get('idcard_name')
    idcard_number = request.form.get('idcard_number')
    project = request.form.get('project')
    file_name = request.form.get('file_name')
    api_provider = request.form.get('api_provider')
    api_config = func.get_api_config('liveness', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    file = func.read_file(file_name)
    if not file:
        raise Exception('文件读取失败')
    if api_provider == 'faceid':
        result = FaceidLiveness.url(idcard_name, idcard_number, file)
    else:
        raise Exception('接口未知')
    func.save_api_log('liveness', result, project, api_provider)
    return {'status': True, 'msg': 'success', 'data': {'url': result}}


def faceid_callback():
    project = request.args.get('project')
    api_provider = request.args.get('api_provider')
    api_config = func.get_api_config('liveness', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("api_config", api_config)
    return FaceidLiveness.callback()