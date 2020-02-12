#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
import base64, json
from api import FaceidIdcardOCR, TencentIdcardOCR, XunfeiIdcardOCR

from system import func
import global_dict


def index():
    side = request.form.get('side')
    project = request.form.get('project')
    file_name = request.form.get('file_name')
    api_provider = request.form.get('api_provider')
    api_config = func.get_api_config('idcard', project, api_provider)
    if not api_config:
        raise Exception('配置错误')
    global_dict.set_value("project", project)
    global_dict.set_value("api_config", api_config)
    file = func.read_file(file_name)
    if not file:
        raise Exception('文件读取失败')
    if api_provider == 'faceid':
        result = FaceidIdcardOCR.ocr(file, side)
    elif api_provider == 'tencent':
        result = TencentIdcardOCR.ocr(file, side)
    elif api_provider == 'xunfei':
        result = XunfeiIdcardOCR.ocr(file, side)
    else:
        raise Exception('接口未知')
    func.save_api_log('idcard', json.dumps(result), project, api_provider)
    return result